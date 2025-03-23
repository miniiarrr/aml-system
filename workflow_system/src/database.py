from typing import Any, Dict, List, Optional
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from loguru import logger
from config import CONFIGS
from datetime import datetime

class MongoDB:
    """
    MongoDB database connector class.
    
    This class handles connection to MongoDB and provides methods
    for interacting with the database collections.
    """
    
    def __init__(self):
        """Initialize the MongoDB connection."""
        self._client = None
        self._db = None
        self._connected = False
    
    async def connect(self) -> bool:
        """
        Connect to the MongoDB database.
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        try:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                CONFIGS.MONGODB.connection_string,
                serverSelectionTimeoutMS=CONFIGS.MONGODB.CONNECTION_TIMEOUT
            )
            
            # Validate connection
            await self._client.server_info()
            self._db = self._client[CONFIGS.MONGODB.DB_NAME]
            self._connected = True
            
            logger.info(f"Connected to MongoDB: {CONFIGS.MONGODB.DB_NAME}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            self._connected = False
            return False
    
    async def disconnect(self) -> None:
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("Disconnected from MongoDB")
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to MongoDB."""
        return self._connected
    
    @property
    def database(self):
        """Get the database instance."""
        if not self._connected:
            logger.warning("Attempting to access database before connection is established")
        return self._db
    
    async def insert_one(self, collection: str, document: Dict[str, Any]) -> Optional[str]:
        """
        Insert a single document into a collection.
        
        Args:
            collection (str): Collection name
            document (Dict[str, Any]): Document to insert
            
        Returns:
            Optional[str]: The ID of the inserted document, or None if insertion failed
        """
        if not self._connected:
            logger.error("Cannot insert document: Not connected to MongoDB")
            return None
        
        try:
            result = await self._db[collection].insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document into {collection}: {str(e)}")
            return None
    
    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document in a collection.
        
        Args:
            collection (str): Collection name
            query (Dict[str, Any]): Query to find document
            
        Returns:
            Optional[Dict[str, Any]]: The found document, or None if not found
        """
        if not self._connected:
            logger.error("Cannot find document: Not connected to MongoDB")
            return None
        
        try:
            result = await self._db[collection].find_one(query)
            return result
        except Exception as e:
            logger.error(f"Error finding document in {collection}: {str(e)}")
            return None
    
    async def find_many(self, collection: str, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        """
        Find multiple documents in a collection.
        
        Args:
            collection (str): Collection name
            query (Dict[str, Any]): Query to find documents
            limit (int, optional): Maximum number of documents to return. Defaults to 0 (no limit).
            
        Returns:
            List[Dict[str, Any]]: List of found documents
        """
        if not self._connected:
            logger.error("Cannot find documents: Not connected to MongoDB")
            return []
        
        try:
            cursor = self._db[collection].find(query)
            if limit > 0:
                cursor = cursor.limit(limit)
            
            results = []
            async for document in cursor:
                results.append(document)
            
            return results
        except Exception as e:
            logger.error(f"Error finding documents in {collection}: {str(e)}")
            return []
    
    async def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """
        Update a single document in a collection.
        
        Args:
            collection (str): Collection name
            query (Dict[str, Any]): Query to find document to update
            update (Dict[str, Any]): Update operations to apply
            
        Returns:
            bool: True if document was updated, False otherwise
        """
        if not self._connected:
            logger.error("Cannot update document: Not connected to MongoDB")
            return False
        
        try:
            result = await self._db[collection].update_one(query, update)
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document in {collection}: {str(e)}")
            return False
    
    async def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """
        Delete a single document from a collection.
        
        Args:
            collection (str): Collection name
            query (Dict[str, Any]): Query to find document to delete
            
        Returns:
            bool: True if document was deleted, False otherwise
        """
        if not self._connected:
            logger.error("Cannot delete document: Not connected to MongoDB")
            return False
        
        try:
            result = await self._db[collection].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document in {collection}: {str(e)}")
            return False
    
    async def watch_collection(self, collection: str, callback, pipeline=None, resume_after=None):
        """
        Watch for changes in a collection and invoke callback for each change.
        
        This method sets up a change stream on the specified collection and calls
        the provided callback function for each change event that occurs.
        
        Args:
            collection (str): Collection name to watch
            callback (callable): Async function to call with each change event
            pipeline (list, optional): Aggregation pipeline for filtering change events
            resume_after (dict, optional): Resume token to resume watching from a specific point
            
        Returns:
            None
        """
        if not self._connected:
            logger.error("Cannot watch collection: Not connected to MongoDB")
            return
        
        try:
            # Set up the change stream
            change_stream = self._db[collection].watch(
                pipeline=pipeline,
                resume_after=resume_after,
                full_document="updateLookup"  # Include the full updated document
            )
            
            logger.info(f"Started watching collection: {collection}")
            
            # Process changes in an infinite loop
            async with change_stream as stream:
                async for change in stream:
                    try:
                        # Call the callback with the change event
                        await callback(change)
                    except Exception as e:
                        logger.error(f"Error in change stream callback: {str(e)}")
                        # Continue watching even if there's an error in the callback
        except Exception as e:
            logger.error(f"Error watching collection {collection}: {str(e)}")

# Create singleton instance
db = MongoDB()

async def setup_transaction_watcher(workflow_manager):
    """
    Set up a change stream watcher for the transactions collection.
    
    This function initializes a MongoDB change stream to watch for
    changes in the transactions collection and forwards those changes
    to the workflow manager for processing.
    
    Args:
        workflow_manager: Instance of the WorkflowManager class
        
    Returns:
        bool: True if the watcher was set up successfully, False otherwise
    """
    if not db.is_connected:
        connected = await db.connect()
        if not connected:
            logger.error("Failed to connect to MongoDB for transaction watching")
            return False
    
    # Create the transactions collection if it doesn't exist
    try:
        # Insert a dummy document to ensure the collection exists, then delete it
        collection_name = "transactions"
        dummy_id = await db.insert_one(collection_name, {
            "dummy": True,
            "created_at": datetime.now()
        })
        if dummy_id:
            await db.delete_one(collection_name, {"_id": dummy_id})
    except Exception as e:
        logger.warning(f"Error ensuring transactions collection exists: {str(e)}")
    
    # Set up the change stream pipeline to only watch for inserts and updates
    pipeline = [
        {"$match": {
            "operationType": {"$in": ["insert"]}
        }}
    ]
    
    # Start watching the transactions collection
    logger.info("Setting up transaction watcher for MongoDB")
    
    async def transaction_callback(change_event):
        """Process a transaction change event."""
        operation_type = change_event.get("operationType")
        logger.info(f"Received {operation_type} event in transactions collection")
        
        # Forward the event to the workflow manager
        await workflow_manager.add_transaction_event(change_event)
    
    # Launch the watcher in a separate task
    import asyncio
    asyncio.create_task(db.watch_collection(
        "transactions", 
        transaction_callback,
        pipeline=pipeline
    ))
    
    logger.info("Transaction watcher set up successfully")
    return True

"""
Usage example:

```python
from src.database import db, setup_transaction_watcher
from src.workflow_manager import WorkflowManager

async def main():
    # Initialize the workflow manager
    workflow_manager = WorkflowManager()
    
    # Set up the transaction watcher
    await setup_transaction_watcher(workflow_manager)
    
    # Connect to MongoDB
    connected = await db.connect()
    if not connected:
        print("Failed to connect to MongoDB")
        return
    
    # ... rest of the code ...
```
""" 
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import { Input } from "@/pages/Input";
import './App.css'
import { TooltipProvider } from "@radix-ui/react-tooltip";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <BrowserRouter>
      <link href='https://fonts.googleapis.com/css?family=Jersey 10' rel='stylesheet'></link>
        <div className="app-container">
          <Routes>
            <Route path="/chart/:txnId" element={<Index />} />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="/search" element={<Input/>} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;

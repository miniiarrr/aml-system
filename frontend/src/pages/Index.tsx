import TreeChart from '@/components/TreeChart';
import './Index.css';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
// SVG circuit graphic for the background

export default function Index() {
  const navigate = useNavigate();

	return (
		<div className="index-container relative">
      <button className="btn-back" onClick={() => navigate('/search')}>
          <ArrowLeft /> Back
        </button>
      <div className="index-cyberpunk-circle"></div>
      <div className="circuit-graphic"></div>
				<TreeChart />
		</div>
	);
}

import { useState, useEffect } from 'react';
import './Content.css';
import { useLocation, useNavigate } from 'react-router-dom';

// CircuitGraphics component for top gate
const TopCircuitGraphics = () => (
  <svg 
    className="circuit-svg top-circuit" 
    viewBox="0 0 500 300" 
    preserveAspectRatio="xMidYMid meet"
  >
    <g className="circuit-paths">
      <path className="circuit-path" d="M297.48,37.261 L305.42,37.261 L319.086,23.594 L330.48,23.594 L330.48,22.177 L351.355,22.177 L351.355,23.594 L403.48,23.594 L393.876,13.99 L297.48,13.99" />
      <path className="circuit-path" d="M23.132,60.927v45.322l5.733,5.733l29.554-29.554h9.936v-1.479h7.25v1.479H95.92l29.811-29.811V34.427H78.98v26.5H56.855v2.375H36.834v-2.375H23.132z" />
      <path className="circuit-path" d="M377.23,25.094v14.372h35.071l57.515,57.515h7.051L404.98,25.094H377.23z" />
      <rect className="circuit-rect" x="239.23" y="31.083" width="40.5" height="2.958" />
      <path className="circuit-path" d="M109.23,14.85v18.078h52.416v-11h25.728l15.333,15.334h8.523v-1.167h18.667v1.167h66.084V13.99H109.23V14.85z" />
      <polygon className="circuit-path" d="M210.73,13.99 L275.064,13.99 L275.064,19.177 L266.064,19.177 L261.939,23.302 L232.564,23.302 L232.564,18.646 L210.73,18.646" />
    </g>
    <g className="circuit-nodes">
      <circle className="circuit-node" cx="175.73" cy="35.302" r="4" />
      <circle className="circuit-node" cx="387.73" cy="32.562" r="4" />
      <circle className="circuit-node" cx="225.73" cy="19.177" r="4" />
      <circle className="circuit-node" cx="112.793" cy="48.719" r="2.5" />
      <circle className="circuit-node" cx="36.835" cy="83.177" r="2.5" />
    </g>
  </svg>
);

// CircuitGraphics component for bottom gate
const BottomCircuitGraphics = () => (
  <svg 
    className="circuit-svg bottom-circuit" 
    viewBox="0 0 500 300" 
    preserveAspectRatio="xMidYMid meet"
  >
    <g className="circuit-paths">
      <path className="circuit-path" d="M33.064,184.51 L64.23,215.677 L69.314,210.594 L85.73,227.01 L85.73,232.177 L113.46,259.906 L143.956,259.906 L157.218,246.644 L157.218,240.01 L148.564,240.01 L148.564,247.656 L140.144,256.076 L120.064,256.076 L120.064,239.177 L105.327,224.441 L97.064,224.441 L97.064,216.344 L74.147,193.427 L67.314,200.26 L52.564,185.51" />
      <path className="circuit-path" d="M361.67,261.677l14.75-14.75h10.561v-13.292h-32.027l-20.292,20.292h-55.917l-8.083-8.083h-14.454l8.273,8.273v7.561h24.25v-2.25h57.375v2.25H361.67z" />
      <path className="circuit-path" d="M172.193,257.079l-16.152,16.152h-8.686v2.32h-8.125v-2.32h-10.689l8.695,8.695h65.684l-12.19-12.189v-12.658H172.193z" />
      <rect className="circuit-rect" x="379.73" y="251.989" width="37.75" height="2.091" />
      <polygon className="circuit-path" d="M126.42,273.232 L107.364,273.232 L23.87,189.738 L23.87,195.469 L110.328,281.927 L135.115,281.927" />
      <path className="circuit-path" d="M404.897,46.927H357.98l-7.5,7.5h-43.75v5h-69.709v-6.406h-78.979v16.342h72.759v3.842H331.23V69.49h47V58.479h20.948l26.927,26.927v6.646h12.771V80.906L404.897,46.927z" />
    </g>
    <g className="circuit-nodes">
      <circle className="circuit-node" cx="357.397" cy="244.115" r="4" />
      <circle className="circuit-node" cx="467.397" cy="277.907" r="4" />
      <circle className="circuit-node" cx="179.536" cy="267.802" r="4" />
      <circle className="circuit-node" cx="88.105" cy="232.177" r="2.5" />
      <circle className="circuit-node" cx="135" cy="256.076" r="2.5" />
    </g>
  </svg>
);

const phrases = [
  'SYSTEM HACKED',
  'REVEALING INFO',
  'ACCESSING BLOCKCHAIN',
  'DATA STREAM OPEN',
];

const Content = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [glitchText, setGlitchText] = useState(phrases[0]);
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate()

  useEffect(() => {
    // Create glitch text effect
    let count = 1;
    const interval = setInterval(() => {
      setGlitchText(phrases[count % phrases.length]);
      count++;
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const toggleGates = () => {
    setIsOpen(prevState => !prevState);
  };

  return (
    <div className="content-container">
      <div className={`gate top-gate ${isOpen ? 'open' : ''}`}>
        <TopCircuitGraphics />
        <div className="gate-design">
          <div className="gate-lines"/>
        </div>
      </div>
      
      <div className={`gate bottom-gate ${isOpen ? 'open' : ''}`}>
        <BottomCircuitGraphics />
        <div className="gate-design">
          <div className="gate-lines"></div>
          <div className="gate-warning">
            <span>AUTHORIZED ACCESS ONLY</span>
            <div className="warning-glow"></div>
          </div>
          <div className="gate-lines"></div>
        </div>
      </div>

      <div className="cyberpunk-circle"></div>
      
      <button 
        className={`access-button ${isOpen ? 'active' : ''}`} 
        onClick={toggleGates}
      >
        <span className="btn-text">{isOpen ? 'LOCK SYSTEM' : 'ACCESS SYSTEM'}</span>
        <span className="btn-glow"></span>
      </button>
      
      <div className={`form-container ${isOpen ? 'visible' : ''}`}>
        <div className="glitch-text">{glitchText}</div>
        <h1>SYSTEM <span className="highlight">ACCESSED</span></h1>
        <div className="input-field">
          <label htmlFor="username">TRANSACTION</label>
          <input value={inputValue} onChange={(e) => setInputValue(e.target.value)} type="text" id="username" placeholder="Enter Transaction ID" />
          <div className="input-scan-line"/>
        </div>
        
        <button className="submit-button" onClick={() => navigate('/chart/' + inputValue)}>
          AUTHENTICATE
          <span className="btn-glow-sm"/>
        </button>
      </div>
    </div>
  );
};

export default Content;

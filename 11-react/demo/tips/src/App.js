import logo from './logo.svg';
import './App.css';

const PAGE_TITLE = `PyBites Python Tips API`;
const TWITTER_ICON = 'https://codechalleng.es/static/img/icon-twitter.9f5315ee958c.png'
function Tip(props) {
    return(
      <div className="tip">
        <p>{props.tip}
        { props.link &&
          <span> (<a href={props.link} target="_blank">source</a>)</span>
        }
        </p>
        <pre>{props.code}</pre>
        { props.share_link &&
	  <p>
	    <a href={props.share_link} target="_blank">
	      <img src={TWITTER_ICON} alt="share"/>
	    </a>
	  </p>
	}
      </div>
    )
}

function App() {
  return (
    <div className="App">
      <h2>{PAGE_TITLE}</h2>
  
      <form id="searchTips">
	<input type="text"
	  placeholder="filter tips"
	  value=''
	  onChange='' />
      </form>

      <div id="tips">
	<Tip tip="123" code="print1" link="http" />
	<Tip tip="456" code="print1"  />
	<Tip tip="789" code="print1" share_link="http" />
      </div>
    </div>
  );
}

export default App;

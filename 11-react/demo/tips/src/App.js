import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

const axios = require('axios')

const PAGE_TITLE = `PyBites Python Tips API`;
const TWITTER_ICON = 'https://codechalleng.es/static/img/icon-twitter.9f5315ee958c.png'
const TIPS_ENDPOINT = 'http://127.0.0.1:8000/api/'

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

class App extends Component {

  constructor(props){
    super(props);
    this.state= {
      orgTips: [],
      showTips: [],
      filterStr: '',
    }
    this.onFilterChange = this.onFilterChange.bind(this);
    this.filterTips= this.filterTips.bind(this);
  }

  componentDidAmount(){
    // call api using axios
    axios.get(TIPS_ENDPOINT)
    .then(response => {
      this.setState({
        orgTips: response.data,
        showTips: response.data
      })
    })
    .catch(function(error){
      console.log(error);
    })
  }

  onFilterChange(event){
    // filter orgTips into showTips
    console.log('onFilterChange called');
  }

  filterTips = (filterStr) => {
    // helper for aonFilterChange
  }

  render() {
    return (
      <div className="App">
        <h2>{PAGE_TITLE}</h2>
    
        <form id="searchTips">
          <input type="text"
            placeholder="filter tips"
            value={this.state.filterStr}
            onChange={this.onFilterChange} />
        </form>
  
        <div id="tips">
          {this.state.showTips.map((tip, index) =>
            <Tip {...tip} key={index} filterStr={this.state.filterStr} />
          )}
        </div>

      </div>
    );
  }
}

export default App;

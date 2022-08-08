import logo from './logo.svg';
import './App.css';
import {Selenium} from './utils/elements'

function App() {
  let selenium = new Selenium({target:'TEST2', props:['text','aria-abel'], action: 'xpath', xpath: [0,0,0,1,2,0,0,0,0,0,0,0,0]});
  let value
  return (
  <div className="YT_FL">


    <div>
      <button onClick = {() => {value = selenium.processAction({selector: 'body'})}}>
        Test
      </button>
      <div>
        <div><div><div><div><div><div><div><div>TEST2</div></div></div></div></div></div></div></div>
      </div>a
      <div>
        <div><div><div><div><div><div><div><div>TEST1</div><div>TEST3</div></div></div></div></div></div></div></div>
      </div>
    </div>
    <div>
      <button onClick = {() => {console.log(value)}}>
        Test
      </button>
      <div>
        <div><div><div><div><div><div><div><div>TEST2</div></div></div></div></div></div></div></div>
      </div>a
      <div>
        <div><div><div><div><div><div><div><div>TEST1</div><div>TEST3</div></div></div></div></div></div></div></div>
      </div>
    </div>
    <div>
      <button onClick = {() => {value = selenium.processAction({selector: 'body'})}}>
        Test
      </button>
      <div>
        <div><div><div><div><div><div><div><div>TEST2</div></div></div></div></div></div></div></div>
      </div>a
      <div>
        <div><div><div><div><div><div><div><div>TEST1</div><div>TEST3</div></div></div></div></div></div></div></div>
      </div>
    </div>
  </div>

  );
}

export default App;

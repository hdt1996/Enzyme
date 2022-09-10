import './App.css';
import {Fetch} from '../src/utils/fetch'
function App() {
  console.log(window.__STATE__)
  let input_value = '<button>HELLO</button>'
  let FETCH = new Fetch("http://192.168.1.86:8001/api/api/1")






  let postFetch = async () =>{  
    FETCH.makeOption({crud:'POST',body:{"field_1":true,"field_2":55,}})
    let data = await FETCH.fetch()
    console.log(data)
  }

  let putFetch = async () =>{  
    FETCH.makeOption({crud:'PUT',body:{"field_1":true,"field_10":90001}, add_headers:{"selectors":{"field_10":{"operator":"equal","value":9000}}}})
    let data = await FETCH.fetch()
    console.log(data)
  }

  let getFetch = async () =>{  
    FETCH.makeOption({crud:'GET',add_headers:{"selectors":{}}})
    let data = await FETCH.fetch()
    console.log(data)
  }
  let deleteFetch = async () =>{  
    FETCH.makeOption({crud:'DELETE',add_headers:{"selectors":{"field_10":{"operator":"equal","value":11}}}})
    let data = await FETCH.fetch()
    console.log(data)
  }
  let field_types = 
  [
    'INT','CHAR','TEXT','FLOAT','FILE','IMG','JSON','BOOL'
  ]

  let renderDrop = (e) =>
  {
    if (e.target.parentNode.childNodes[1].classList.contains('TY_HID'))
    {
      e.target.parentNode.childNodes[1].classList.remove('TY_HID')
    }
    else{
      e.target.parentNode.childNodes[1].classList.add('TY_HID')
    }
  }
  return (
<div className = "YT_bdWH1px YT_bdDash YT_FX YT_FXR YT_H100vh YT_W100vw YT_bckgGRA">


  <div className = "YT_bdWH1px YT_bdDash YT_FXR YT_FX1">

  </div>

  <div className = "YT_bdWH1px YT_bdDash YT_FX YT_FXC YT_FX5">
    <div className = "YT_FX1 YT_bdWH1px YT_bdDash YT_FX YT_FXC YT_FXAIC">
    </div>
    <div className = "YT_FX1 YT_bdWH1px YT_bdDash">
      <div className = "TY_FX1 YT_bckgWH">
      <button onClick = {() => {postFetch()}}>POST</button>
      <button onClick = {() => {getFetch()}}>GET</button>
      <button onClick = {() => {putFetch()}}>PUT</button>
      <button onClick = {() => {deleteFetch()}}>DELETE</button>
      <input placeholder = 'BODY'></input>
      <div>
        <div>

          {input_value}
        </div>
      </div>
      <div className = "TY_DD">
        <div onClick = {(e) =>{renderDrop(e)}}>Dropdown</div>
        <div className = "TY_DI TY_HID">
          {field_types.map((field,f_index) =>
          {
            return(
              <div  key= {f_index} className = "TY_DII" >
                <button>{field}</button>
              </div>
            )
          })}
        </div>
      </div>
      </div>
    </div>
    <div className = "YT_FX1 YT_bdWH1px YT_bdDash">
      <div className = "TY_FX1 YT_bckgWH">

      </div>
    </div>
  </div>

  <div className = "YT_bdWH1px YT_bdDash YT_FXR YT_FX1">

  </div>


</div>
  );
}

export default App;

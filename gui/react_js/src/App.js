import logo from './logo.svg';
import './App.css';
import {Selenium} from './utils/elements'

function App() {

  let postoptions = 
  {
    method: 'POST',
    headers:{'Content-Type': 'application/json'},
    body: JSON.stringify(
      
        {
          "field_1":true,
          "field_2":55,
        }
      
    ),
  }



  let putoptions = 
  {
    method: 'PUT',
    headers:{
      'Content-Type': 'application/json',
      'selectors':JSON.stringify({"field_10":{"operator":"equal","value":9000}}),
    },
    body: JSON.stringify(
      {
        "field_1":true,
        "field_10":90001
      }
    
    ),
  }

  let deleteoptions = 
  {
    method: 'DELETE',
    headers:{
      'Content-Type': 'application/json',
      'selectors':JSON.stringify({"field_10":{"operator":"equal","value":11}}),
    }
  }
  let getoptions = 
  {
    method: 'GET',
    headers:{
      'Content-Type': 'application/json',
      'selectors':JSON.stringify({"field_3":{"operator":"equal","value":"OELPAEJYVBWKDSNQZDTYIXZOEQEOLKGPLWSPQNAPYGCPLRZZFYGNPUOZYCKDKXHHBHVEFYQVEHINNTVSHYHMGFPPCYIVNQGIYJAEDKIFCWWZHAREYQEJDNSSHCPWZGVHISROUDMPONNLUJDHHGJAHSFZDCXCLELQZDCEYWMOKVTEIYLIPLKYFZCJIGKWKGSQNCMFTXBGWIEIMJCNVMYDCNQRCLDABNMDSAKIQVBHMYROYXHFEXJEYUOHNLXFYPB"}})},
  }

  let getFetch = async () =>{  
    let response = await fetch("http://192.168.1.86:8001/api/api/1", getoptions)
    let data = await response.json()
    console.log(data)
  }

  let postFetch = async () =>{  
    let response = await fetch("http://192.168.1.86:8001/api/api/1", postoptions)
    let data = await response.json()
    console.log(data)
  }

  let putFetch = async () =>{  
    let response = await fetch("http://192.168.1.86:8001/api/api/1", putoptions)
    let data = await response.json()
    console.log(data)
  }
  let deleteFetch = async () =>{  
    let response = await fetch("http://192.168.1.86:8001/api/api/1", deleteoptions)
    let data = await response.json()
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




{/* <div className = "YT_bdWH1px YT_bdDash YT_FX YT_H100vw YT_W100vw YT_bckgBL YT_OP50">

<div className = "YT_FX1 YT_bdWH1px YT_bdDash YT_H100pc"></div>

<div className = "YT_FX7 YT_bdWH1px YT_bdDash YT_bckgBLK YT_OP80 YT_FX YT_FXC YT_H100pc">
  <div className = "YT_bdWH1px YT_bdDash YT_FXC YT_F1"></div>
  <div className = "YT_bdWH1px YT_bdDash YT_FXC YT_F1"></div>
  <div className = "YT_bdWH1px YT_bdDash YT_FXC YT_F1"></div>
</div>

<div className = "YT_FX1 YT_bdWH1px YT_bdDash YT_H100pc"></div>
</div> */}
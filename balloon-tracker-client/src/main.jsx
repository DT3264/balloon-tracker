import React from 'react'
import ReactDOM from 'react-dom/client'
import { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App (){
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(undefined);
  const [checkedItems, setCheckedItems] = useState([]);
  const getUrl = () => {
    // Commented out when testing individually
    let baseUrl = "http://127.0.0.1:8000";
    // Commented out when serving from the backend
    // let baseUrl = window.location.href;
    if (baseUrl.endsWith("/")) {
      baseUrl = baseUrl.slice(0, -1);
    }
    return baseUrl;
  };
  const fetchData = async () => {
    setLoading(true);
    axios.get(`${getUrl()}/get-data/`)
    .then(result => {
      setData(result.data.data);
      setError(undefined);
      setLoading(false);
    })
    .catch(error => {
      console.error(error)
      setError(error);
      setLoading(false);
    });
  };
  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 10*1000);

    return () => clearInterval(interval);
  }, []);


  const sortedData = [...data].sort((a, b) => {
    const aChecked = checkedItems.includes(a.username);
    const bChecked = checkedItems.includes(b.username);
    if (aChecked && !bChecked) {
      return -1;
    } else if (!aChecked && bChecked) {
      return 1;
    } else {
      return 0;
    }
  });
  const onClick=(username, problemIdx, problemStatus)=>{
    if(problemStatus === 0 || problemStatus === 2) return;
    const confirmed = window.confirm(`Confirming updating problem ${String.fromCharCode(65+problemIdx)} for ${username}?`);
    if (confirmed) {
      axios.post(`${getUrl()}/update-submission`, {
          'username': username,
          'problem_index': problemIdx
      })
      .then(_ => fetchData())
      .catch(error => console.error(error));
    }
  }

  const problemCount = data.length > 0 ? data[0].problems.length : 0;
  const problemHeaders = []
  for(var i = 0; i<problemCount; i++){
    problemHeaders.push(String.fromCharCode(65+i));
  }
  return (<div>
      {loading ? <p>Loading data</p> : <></>}
      {error !== undefined ? <p>Error loading data, see the console for more information</p> : <></>}
      <Table bordered={true}>
        <thead>
          <tr>
            <th>On top</th>
            <th>Username</th>
            {problemHeaders.map(header => <th key={header}>{header}</th>)}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row) => {
            return <tr key={row.username}>
              <td>
                <input type="checkbox" checked={checkedItems.includes(row.username)} onChange={(e) => {
                  if (e.target.checked) {
                    setCheckedItems([...checkedItems, row.username]);
                  } else {
                    setCheckedItems(checkedItems.filter((username) => username !== row.username));
                  }
                }} />
              </td>
              <td>{row.username}</td>
              {row.problems.map((problemStatus, index)=>{
                let backgroundColor = "white";
                if(problemStatus === 1) backgroundColor = "orange";
                if(problemStatus === 2) backgroundColor = "lawngreen";
                return <td 
                  className='m-1'
                  key={`${row.username}${index}`} 
                  onClick={()=>onClick(row.username, index, problemStatus)}
                  style={{ backgroundColor: backgroundColor}}>
                  {problemStatus}
                </td>
              })}
            </tr>
          })}
        </tbody>
      </Table>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>,
)

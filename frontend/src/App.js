import './App.css';
import React, { useState, useEffect } from 'react';

const App = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000');
        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`);
        }
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);
  return (
      <table className="table table-bordered">
        <tbody>
        <tr>
          <th rowSpan="2">Building</th>
          <th rowSpan="2">Rent</th>
          <th rowSpan="2">Deposit</th>
          <th rowSpan="2">Amenities</th>
          <th colSpan="2">Spaces</th>
        </tr>
        <tr>
          <th>Name</th>
          <th>Status</th>
        </tr>
        {data.map((entry, index) => (
            <React.Fragment key={index}>
              <tr>
                <td rowSpan={entry.Spaces.length + 1}>{entry.Building}</td>
                <td rowSpan={entry.Spaces.length + 1}>{entry.Rent}</td>
                <td rowSpan={entry.Spaces.length + 1}>{entry.Deposit}</td>
                <td rowSpan={entry.Spaces.length + 1}>{entry.Amenities}</td>
              </tr>
              {entry.Spaces.map((space, spaceIndex) => (
                  <tr key={`${index}-${spaceIndex}`}>
                    <td>{space.Name}</td>
                    <td>{space.Status}</td>
                  </tr>
              ))}
            </React.Fragment>
        ))}
        </tbody>
      </table>
  );
}

export default App;

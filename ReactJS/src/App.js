import './App.css';
import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";
export const options = {
  title: "Feedback data from SQL database",
  titleTextStyle: {
    color: "white"
  },
  legend: {
    textStyle: { color: "white" }
  },
  is3D: true,
  backgroundColor: 'transparent',
  fontSize: "25",
  fontName: "Nirmala UI",
  slices: {
    0: { color: "#B6E2A1" },
    1: { color: "#FFC898" },
    2: { color: "#BB6464" },
  },
};

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://192.168.0.103:5000/feedbacko")
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  const [feedbackData, setFeedbackData] = useState([])

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://192.168.0.103:5000/feedback")
        .then(res => (res.json()))
        .then(
          (result) => {
            setFeedbackData(result);
          },
        )
    }, 3000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <div>
      <Chart
        chartType="PieChart"
        data={[["Feedback", "Count"], ["Satisfied", feedbackData.good], ["Neutral", feedbackData.mid], ["Unsatisfied", feedbackData.bad]]}
        options={options}
        width={"100%"}
        height={"500px"}
      />


      <table>
        <thead>
          <tr>
            <th>FEEDBACK</th>
            <th>MAC</th>
            <th>TIME</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.feedback}</td>
              <td>{item.mac}</td>
              <td>{item.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


export default App
import "./App.css";
import React, { useState, useEffect } from "react";
import LoadingIcon from "./LoadingIcon";

const App = () => {
	const [data, setData] = useState([]);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await fetch("https://chapter-booking-webscraper-backend.vercel.app/");
				if (!response.ok) {
					throw new Error(`API request failed with status ${response.status}`);
				}
				const jsonData = await response.json();
				setData(jsonData);
			} catch (error) {
				console.error("Error fetching data:", error);
			} finally {
				setIsLoading(false); // Set loading indicator to false after fetching
			}
		};
		fetchData();
	}, []);
	return (
		<div>
			<h1>Chapter Living Scraped Data</h1>
			{isLoading ? (
				<LoadingIcon /> // Display loading icon while data is being fetched
			) : (
				<table className="table table-bordered">
					<tbody>
						<tr>
							<th rowSpan="2">Sr. No.</th>
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
									<td rowSpan={entry.Spaces.length + 1}>{index + 1}</td>
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
			)}
		</div>
	);
};

export default App;

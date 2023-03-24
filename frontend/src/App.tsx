import "./App.css";
import FileUpload from "./components/upload";
import Tabs from "./components/tabs";

const App = () => {
	return (
		<div id="App">
			<div id="left-side">
				<FileUpload />
			</div>
			<div id="right-side">
				<Tabs />
			</div>
		</div>
	);
};

export default App;

import "./App.css";
import FileUpload from "./components/upload";
import Tabs from "./components/tabs";
import { useState } from "react";

const App = () => {
	const [audioBlob, setAudioBlob] = useState("");

	return (
		<div id="App">
			<div id="left-side">
				<FileUpload setAudioBlob={setAudioBlob} />
			</div>
			<div id="right-side">
				<Tabs audioBlob={audioBlob} />
			</div>
		</div>
	);
};

export default App;

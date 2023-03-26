import "./App.css";
import FileUpload from "./components/upload";
import Tabs from "./components/tabs";
import { useState } from "react";

const App = () => {
	const post_text =
		"will be automatically generated when files are uploaded and processed on our servers";
	const [audioBlob, setAudioBlob] = useState<string>("");
	const [transcription, setTranscription] = useState<string>(
		`Transcription ${post_text}`,
	);
	const [summary, setSummary] = useState<string>(`Summary ${post_text}`);
	const [question, setQuestion] = useState<string>("");
	const [answer, setAnswer] = useState<string>("");

	return (
		<div id="App">
			<div id="left-side">
				<FileUpload
					setAudioBlob={setAudioBlob}
					setTranscription={setTranscription}
					setSummary={setSummary}
				/>
			</div>
			<div id="right-side">
				<Tabs
					audioBlob={audioBlob}
					summary={summary}
					transcription={transcription}
					question={question}
					setQuestion={setQuestion}
					answer={answer}
					setAnswer={setAnswer}
				/>
			</div>
		</div>
	);
};

export default App;

import "./styles.css";
import { useState } from "react";
import Transcription from "./transcription";
import CustomAudio from "../audio/index";
import Summary from "./summary";
import Qa from "./qa";
import Prompt from "../prompt";

// interface TabsData {
// 	audioBlob: string;
// 	transcription: string;
// 	summary: string;
// 	question: string;
// 	setQuestion: string;
// }

const Tabs = ({
	audioBlob,
	transcription,
	summary,
	question,
	setQuestion,
	answer,
	setAnswer,
}) => {
	const [state, setState] = useState({
		showTranscription: true,
		showSummary: false,
		showQA: false,
	});

	return (
		<div id="tabs-container">
			<div id="inner-container">
				<div id="top-section">
					<button
						className="top-section-buttons"
						style={
							state.showTranscription
								? { backgroundColor: "#A020F0", color: "#fff" }
								: {}
						}
						onClick={() =>
							setState({
								showTranscription: true,
								showSummary: false,
								showQA: false,
							})
						}
					>
						Transcription
					</button>
					<button
						className="top-section-buttons"
						style={
							state.showSummary
								? { backgroundColor: "#A020F0", color: "#fff" }
								: {}
						}
						onClick={() =>
							setState({
								showTranscription: false,
								showSummary: true,
								showQA: false,
							})
						}
					>
						Summary
					</button>
					<button
						className="top-section-buttons"
						style={
							state.showQA ? { backgroundColor: "#A020F0", color: "#fff" } : {}
						}
						onClick={() =>
							setState({
								showTranscription: false,
								showSummary: false,
								showQA: true,
							})
						}
					>
						Questioning
					</button>
				</div>

				<div id="mid-section">
					{state.showTranscription ? (
						<Transcription transcription={transcription} />
					) : state.showSummary ? (
						<Summary summary={summary} />
					) : state.showQA ? (
						<Qa question={question} answer={answer} />
					) : (
						"Browse"
					)}
				</div>

				<div id="bottom-section">
					{state.showQA ? (
						<Prompt
							question={question}
							setQuestion={setQuestion}
							transcription={transcription}
							setAnswer={setAnswer}
							answer={answer}
						/>
					) : (
						<CustomAudio audioBlob={audioBlob} />
					)}
				</div>
			</div>
		</div>
	);
};

export default Tabs;

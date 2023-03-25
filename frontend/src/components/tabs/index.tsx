import { useState } from "react";
import "./styles.css";
import Summary from "./summary";
import Transcription from "./transcription";
import Qa from "./qa";
import CustomAudio from "../audio/index";
import Prompt from "../prompt";

interface AudioBlob {
	audioBlob: string;
}

const Tabs = ({ audioBlob }: AudioBlob) => {
	const [state, setState] = useState({
		showTranscription: false,
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
						<Transcription />
					) : state.showSummary ? (
						<Summary />
					) : state.showQA ? (
						<Qa />
					) : (
						"Browse"
					)}
				</div>

				<div id="bottom-section">
					{state.showQA ? <Prompt /> : <CustomAudio audioBlob={audioBlob} />}
				</div>
			</div>
		</div>
	);
};

export default Tabs;

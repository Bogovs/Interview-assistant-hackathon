import React, { useState } from "react";

// interface IQa {
// 	transcription: string;
// 	question: string;
// 	setQuestion: string;
// }
import { endpoint } from "../../constants";

const Qa = ({ question, answer }) => {
	return (
		<div>
			{answer === "" || answer === undefined ? (
				<>
					<section>{question}</section>
					<p>
						Click the <b>"Browse"</b> button to Load your interview, click the
						<b>"Upload"</b> Button to send it on our server, we'll Transcribe
						it, then, you can ask related questions regarding the interview
					</p>
				</>
			) : (
				<>
					<section style={{ marginBottom: "1rem", fontSize: "1.4rem" }}>
						<b>{question}</b>
					</section>
					{answer}
				</>
			)}
		</div>
	);
};

export default Qa;

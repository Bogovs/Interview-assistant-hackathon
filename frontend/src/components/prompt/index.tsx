import "./styles.css";
import { endpoint } from "../constants";

const Prompt = ({ transcription, question, setQuestion, setAnswer }) => {
	const handleSubmit = async (ev) => {
		ev.preventDefault();
		console.log(transcription);
		if (transcription !== "" && transcription !== undefined) {
			var myHeaders = new Headers();
			myHeaders.append("Content-Type", "application/json");

			let raw = JSON.stringify({
				transcription: transcription,
				question: question,
			});

			fetch(endpoint.prompt, {
				method: "POST",
				headers: myHeaders,
				body: raw,
				redirect: "follow",
			})
				.then((response) => response.json())
				.then((result) => setAnswer(result.answer))
				.catch((error) => setAnswer(`Error Occured! ${error}`));
		} else {
			return;
		}
	};

	return (
		<form onSubmit={handleSubmit} id="form">
			<input
				id="user-prompt"
				type="text"
				placeholder="Ask Questions Regarding the Interview"
				value={question}
				onChange={(event) => setQuestion(event.target.value)}
			/>
			<button type="submit" id="ask-button">
				Ask
			</button>
		</form>
	);
};

export default Prompt;

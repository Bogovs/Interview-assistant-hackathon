import { AudioBlob } from "../props.types";
import "./styles.css";

const CustomAudio = ({ audioBlob }: AudioBlob) => {
	return (
		<>
			<audio id="audio-player" src={audioBlob} controls />
		</>
	);
};

export default CustomAudio;

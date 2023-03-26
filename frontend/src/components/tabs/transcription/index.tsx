interface ITranscription {
	transcription: string;
}

const Transcription = ({ transcription }: ITranscription) => {
	return <div>{transcription}</div>;
};

export default Transcription;

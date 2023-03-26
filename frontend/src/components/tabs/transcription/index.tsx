interface ITranscription {
	transcription: string;
}

const Transcription = ({ transcription }: ITranscription) => {
	// rome-ignore lint/security/noDangerouslySetInnerHtml: <explanation>
	return <div dangerouslySetInnerHTML={{ __html: transcription }} />;
};

export default Transcription;

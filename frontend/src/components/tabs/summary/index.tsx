interface ISummary {
	summary: string;
}

const Summary = ({summary}: ISummary) => {
	return <div>{summary}</div>;
};

export default Summary;

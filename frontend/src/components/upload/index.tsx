import { ChangeEvent, useState } from "react";
import { fetchEndpoint } from "../utils";
import { endpoint, formats } from "../constants";
import "./styles.css";

// Handles File Upload
const FileUpload = () => {
	const [file, setFile] = useState<File>();

	// Choose File to Upload
	const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
		if (e.target.files) {
			setFile(e.target.files[0]);
		}
	};

	// Ensure Valid Audio FileType, then, Upload to the server
	const handleUpload = () => {
		console.log(file);
		if (!file) {
			return;
		}

		if (formats.includes(file.type)) {
			console.log("Upload Audio File to the Server!");
			// fetchEndpoint(endpoint.audioUpload, file);
		} else {
			console.log("Invalid File Format!");
		}
	};

	return (
		<div>
			<input
				type="file"
				id="upload-input"
				multiple={false}
				title="Upload Audio File"
				accept="audio/wav, audio/mp3, audio/falc"
				onChange={handleFile}
			/>
			<div>{file && `${file.name}`}</div>
			<button onClick={handleUpload}>Upload</button>
		</div>
	);
};

export default FileUpload;

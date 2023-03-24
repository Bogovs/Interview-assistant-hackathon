import { ChangeEvent, useState, useRef } from "react";
import { fetchEndpoint } from "../utils";
import { endpoint, formats } from "../constants";
import "./styles.css";

// Handles File Upload
const FileUpload = () => {
	const [file, setFile] = useState<File>();
	const uploadInput = useRef<HTMLInputElement>(null);

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

	const simulateBrowse = () => {
		uploadInput.current?.click();
	};

	return (
		<div id="upload-container">
			<input
				ref={uploadInput}
				type="file"
				multiple={false}
				id="actual-file-input"
				title="Upload Audio File"
				accept="audio/wav, audio/mp3, audio/falc"
				onChange={handleFile}
			/>
			{/* rome-ignore lint/a11y/useKeyWithClickEvents: <explanation> */}
			<div id="upload-input" onClick={simulateBrowse}>
				<div id="browse-wrapper">
					<button id="browse-button" onClick={simulateBrowse}>
						Browse
					</button>
					<div id="file-metadata">{file && `${file.name}`}</div>
				</div>
			</div>
			<button onClick={handleUpload}>Upload</button>
		</div>
	);
};

export default FileUpload;

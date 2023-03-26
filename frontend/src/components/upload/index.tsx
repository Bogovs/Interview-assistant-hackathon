import { ChangeEvent, useState, useRef, useEffect } from "react";
import { fetchEndpoint } from "../utils";
import { endpoint, formats } from "../constants";
import "./styles.css";

// interface IFileUpload {
// 	setAudioBlob: string;
// }

// Handles File Upload
const FileUpload = ({ setAudioBlob, setTranscription, setSummary }) => {
	const [file, setFile] = useState<File>();
	const [uploadIndicator, setUploadIndicator] = useState<string>("...");
	const uploadInput = useRef<HTMLInputElement>(null);

	// Choose File to Upload
	const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
		if (e.target.files) {
			setAudioBlob(URL.createObjectURL(e.target.files[0]));
			setFile(e.target.files[0]);
		}
	};

	const fetching = (formdata: FormData) => {
		fetch(endpoint.audioUpload, {
			method: "POST",
			body: formdata,
			redirect: "follow",
		})
			.then((response) => response.json())
			.then((result) => {
				setTranscription(result.output.html);
				setSummary(result.output.summary);
			})
			.catch((error) => {
				return error;
			});
	};

	// Ensure Valid Audio FileType, then, Upload to the server
	const handleUpload = () => {
		console.log(file);
		if (!file) {
			console.log("!file");
			return;
		}

		if (!formats.includes(file.type)) {
			console.log("Invalid File Format!");
		}

		console.log("Upload Audio File to the Server!");

		let formdata = new FormData();
		formdata.append("audio_file", file);
		fetching(formdata);
	};

	const simulateBrowse = () => {
		uploadInput.current?.click();
	};

	return (
		<div id="upload-container">
			<form>
				<input
					ref={uploadInput}
					type="file"
					multiple={false}
					id="actual-file-input"
					title="Upload Audio File"
					accept="audio/wav, audio/mp3"
					onChange={handleFile}
				/>
			</form>
			{/* rome-ignore lint/a11y/useKeyWithClickEvents: <explanation> */}
			<div id="upload-input" onClick={simulateBrowse}>
				<div id="browse-wrapper">
					<button id="browse-button" onClick={simulateBrowse}>
						Browse
					</button>
					<div id="file-metadata">{file && `${file.name}`}</div>
				</div>
			</div>
			{uploadIndicator} <br /> <br />
			<button
				onClick={handleUpload}
				className="top-section-buttons"
				style={{ backgroundColor: "#A020F0", color: "#fff" }}
			>
				Upload
			</button>
		</div>
	);
};

export default FileUpload;

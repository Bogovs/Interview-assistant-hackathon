/**
 * Sends Form Data via POST Request
 *
 * @param {string} url - endpoint url
 * @param {File} file - audio file
 * @returns {any}
 */
const fetchEndpoint = (url: string, file: File): any => {
	let formdata = new FormData();
	formdata.append("audio_file", file);

	fetch(url, {
		method: "POST",
		body: formdata,
		redirect: "follow",
	})
		.then((response) => response.json())
		.then((result) => {return result})
		.catch((error) => {return error});
};

export { fetchEndpoint };

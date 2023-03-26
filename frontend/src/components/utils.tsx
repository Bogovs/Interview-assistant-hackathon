/**
 * Sends Form Data via POST Request
 *
 * @param {string} url - endpoint url
 * @param {File} file - audio file
 * @returns {void}
 */
const fetchEndpoint = (url: string, file: File): void => {
	var formdata = new FormData();
	formdata.append("audio_file", file);

	fetch(url, {
		method: "POST",
		body: formdata,
		redirect: "follow",
	})
		.then((response) => response.text())
		.then((result) => console.log(result))
		.catch((error) => console.log("error", error));
};

export { fetchEndpoint };

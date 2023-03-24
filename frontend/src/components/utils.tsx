/**
 * Sends Form Data via POST Request
 *
 * @param {string} url - endpoint url
 * @param {File} file - audio file
 * @returns {void}
 */
const fetchEndpoint = (url: string, file: File): void => {
	let formData = new FormData();
	formData.append("file", file);
	fetch(url, {
		method: "POST",
		body: formData,
		redirect: "follow",
		headers: {
			"content-type": file.type,
		},
	})
		.then((res) => res.json())
		.then((data) => console.log(data))
		.catch((error) => console.log(error));
};

export { fetchEndpoint };

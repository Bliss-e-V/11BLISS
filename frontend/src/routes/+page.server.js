export const actions = {
	search: async ({ cookies, request }) => {
		const data = await request.formData();
		const address = data.get('address');
		const date = data.get('date');
		const time = data.get('time');
        console.log("Adress: " + address);
		console.log("Date: " + date);
		console.log("Time: " + time);
		return { success: true };
	},

};
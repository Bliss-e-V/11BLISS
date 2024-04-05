export const actions = {
	search: async ({ cookies, request }) => {
		const data = await request.formData();
		const address = data.get('address');
        console.log(address); 
		return { success: true };
	},

};
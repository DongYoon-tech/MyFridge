$('.delete-ingredient').click(deleteIngredient);

async function deleteIngredient() {
	const id = $(this).data('id');
	await axios.delete(`/user/ingredient/${id}/delete`);
	$(this).parent().parent().remove();
}

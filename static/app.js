$('.delete-ingredient').click(deleteIngredient);

async function deleteIngredient() {
    const id = $(this).data('id');
    let $container = $('#ingredientList');
    let res = await axios.delete(`/user/ingredient/${id}/delete`);
    let $item = `<div class="alert alert-danger">Item ${res.data.message}</div>`;
    $container.before($item);
    $(this).parent().parent().remove();
}

// // work below need imrpovements
// $('.star').click(star);
// async function star(evt) {
// 	const $tgt = $(evt.target);
// 	const id = $(this).data('id');
// 	// console.log(id);
// 	if ($tgt.hasClass('fas')) {
// 		let res = await axios.delete(`/user/recipe/${id}/favorites`);
// 		$tgt.toggleClass('fas far');
// 	} else {
// 		let res = await axios.post(`/user/recipe/${id}/favorites`);
// 		$tgt.toggleClass('fas far');
// 	}
// }

// $('.thumbs').click(thumbs);
// async function thumbs(evt) {
// 	const $tgt = $(evt.target);

// 	if ($tgt.hasClass('fas')) {
// 		$tgt.toggleClass('fas far');
// 	} else {
// 		$tgt.toggleClass('fas far');
// 	}
// }

//thumbs up <i class="fas fa-thumbs-up"></i>

// reference from hack or snooze

// $('.articles-container').on('click', '.star', async function(evt) {
// 	if (currentUser) {
// 		const $tgt = $(evt.target);
// 		const $closestLi = $tgt.closest('li');
// 		const storyId = $closestLi.attr('id');

// 		// if the item is already favorited
// 		if ($tgt.hasClass('fas')) {
// 			// remove the favorite from the user's list
// 			await currentUser.removefavs(storyId);
// 			console.log(this);
// 			// then change the class to be an empty star
// 			$tgt.closest('i').toggleClass('fas far');
// 		} else {
// 			// the item is un-favorited
// 			await currentUser.addfavs(storyId);
// 			$tgt.closest('i').toggleClass('fas far');
// 		}
// 	}
// });

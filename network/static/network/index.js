document.addEventListener('DOMContentLoaded', async () => {
    makePagesNavigationBar();
    await getPages(1);
    makeNewPostFunctionality();
});
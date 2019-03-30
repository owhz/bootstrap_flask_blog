

function getOffset(el) {

    el = el.getBoundingClientRect();

    return {
        x: el.left + window.scrollX,
        y: el.top + window.scrollY
    }
}



function scrollToCategoryHeading(categoryHeadingId, event) {

    for (let i in this.$refs) {
        let el = this.$refs[i];
        el.classList.remove("active");
    }

    let el = document.getElementById(categoryHeadingId);
    if (el) {
        let offset = this.getOffset(el);
        window.scroll({top: offset.y - 68, left: offset.x, behavior: "smooth"});
    }
    event.target.classList.add("active");
}

function setActiveCategoryHeading() {

}

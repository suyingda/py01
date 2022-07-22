const intl_get_all_a = document.getElementsByClassName('__dumi-default-previewer-actions')
const intl_change_a_click = Array.from(intl_get_all_a);
if (intl_change_a_click) {
    intl_change_a_click.forEach((item) => {
        const a_tag = item.getElementsByTagName('a')
        if (a_tag && a_tag[0]) {
            const split_localhost = a_tag[0].href.split('~demos')
            split_localhost[0] = 'http://intl-design-ui.woa.com/~demos';
            a_tag[0].addEventListener('click', function () {
                window.location.href = split_localhost.join('')
            })
        }

    })
}

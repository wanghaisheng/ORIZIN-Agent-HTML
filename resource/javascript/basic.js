async function readable_text_setting() {
    const use_bold_text = await eel.read_setting("bold_text")();
    if (use_bold_text === "True") {
        document.body.style.fontWeight = "bold";
    }
    const use_bigger_text = await eel.read_setting("bigger_text")();
    if (use_bigger_text === "True") {
        document.body.style.fontSize = "1.1em";
    }
}

$(function() {
    $("header").load("basic.html");
    $.ripple(".ripple_effect", {
        debug: false,
        on: 'mousedown',
        opacity: 0.4,
        color: "auto",
        multi: false,
        duration: 0.7,
        rate: function(pxPerSecond) {
            return pxPerSecond;
        },
        easing: 'linear'
    });
    readable_text_setting();
});
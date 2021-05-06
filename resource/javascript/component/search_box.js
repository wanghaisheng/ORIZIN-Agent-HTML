class SearchBox extends HTMLElement {
    constructor() {
        super();

        const input_event = new Event("input");

        const shadow = this.attachShadow({ mode: "open" });

        const outer_element = document.createElement("div");
        outer_element.setAttribute("id", "outer");

        const search_icon_outer = document.createElement("div");
        search_icon_outer.setAttribute("id", "search_icon_outer");

        const search_icon_element = document.createElement("i");
        search_icon_element.textContent = "search";
        search_icon_element.setAttribute("id", "search_icon");
        search_icon_element.setAttribute("class", "material_icon");

        this.text_box_outer = document.createElement("div");
        this.text_box_outer.setAttribute("id", "text_box_outer");

        this.text_box = document.createElement("input");
        this.text_box.setAttribute("id", "search_box");
        this.text_box_outer_width = {
            not_entered: "calc(100% - 2rem)",
            entered: "calc(100% - 3.6rem)"
        };
        this.text_box.setAttribute("placeholder", "設定項目を検索");
        this.text_box.addEventListener("input", () => {
            const value = this.text_box.value;
            this.setAttribute("value", value);
            this.dispatchEvent(input_event);
            if (value) {
                this.clear_icon_outer.style.display = "inline-block";
                this.text_box_outer.style.width = this.text_box_outer_width.entered;
            } else {
                this.clear_icon_outer.style.display = "none";
                this.text_box_outer.style.width = this.text_box_outer_width.not_entered;
            }
        });
        this.text_box.addEventListener("focusin", () => {
            outer_element.classList.add("focused");
        });
        this.text_box.addEventListener("focusout", () => {
            outer_element.classList.remove("focused");
        });

        this.clear_icon_outer = document.createElement("div");
        this.clear_icon_outer.setAttribute("id", "clear_icon_outer");

        const clear_icon_element = document.createElement("mwc-icon-button");
        clear_icon_element.setAttribute("icon", "clear");
        clear_icon_element.setAttribute("id", "clear_icon");
        clear_icon_element.addEventListener("click", () => {
            this.setAttribute("value", "");
        });

        const style_element = document.createElement("style");
        style_element.textContent = `
#outer {
    background: var(--card_bg);
    width: 50%;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    position: relative;
    top: 0;
    left: 0;
    overflow: visible;
}

#outer::before {
    content: "";
    display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    border-radius: 0.25rem;
    border: solid 1px var(--text);
    opacity: 0.2;
    pointer-events: none;
    transition: 0.3s;
}

#outer.focused::before {
    border: solid 1px var(--theme_color);
    opacity: 0.75;
}

.material_icon {
    font-family: "Material Icons";
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    transform: translateY(0.15em);
    color: var(--text);
}

#search_icon_outer {
    padding: 0 0.5rem;
    width: 1rem;
    height: 1.5rem;
    display: inline-block;
}

#search_icon {
    cursor: default;
    transition: 0.3s;
}

#text_box_outer {
    width: ${this.text_box_outer_width.not_entered};
    height: 1.75rem;
    display: inline-block;
}

#outer.focused #search_icon {
    color: var(--theme_color);
}

#search_box {
    width: 100%;
    height: 100%;
    background: transparent;
    outline: none;
    border: none;
    color: var(--text);
    padding: 0;
}

#search_box:placeholder {
    color: var(--text);
    opacity: 0.5;
}

#clear_icon_outer {
    display: none;
    width: 1.5rem;
    height: 1.5rem;
    vertical-align: super;
}

#clear_icon {
    cursor: pointer;
    --mdc-icon-button-size: 1.5rem;
    --mdc-icon-size: 1rem;
}
        `;

        search_icon_outer.appendChild(search_icon_element);
        this.text_box_outer.appendChild(this.text_box);
        this.clear_icon_outer.appendChild(clear_icon_element);
        outer_element.appendChild(search_icon_outer);
        outer_element.appendChild(this.text_box_outer);
        outer_element.appendChild(this.clear_icon_outer);
        shadow.appendChild(outer_element);
        shadow.appendChild(style_element);
    }

    init(selector) {
        document.querySelectorAll(selector).forEach((element) => {
            const display_property = getComputedStyle(element).getPropertyValue("display");
            element.dataset.defaultDisplayProperty = display_property;
        });

        this.addEventListener("input", () => {
            const query = this.normalize_text(this.value);

            document.querySelectorAll(selector).forEach((element) => {
                const content_text = this.normalize_text(element.innerText);
                const default_display_property = element.dataset.defaultDisplayProperty;
                const is_match = content_text.indexOf(query) === -1;
                element.style.display = is_match ? "none" : default_display_property;

                const search_tag_string = element.dataset.searchTag;
                if (!search_tag_string) return;
                const search_tag = search_tag_string.replaceAll(", ", ",").replaceAll("  ", " ").replaceAll(" ", ",").split(",");
                for (let i = 0; i < search_tag.length; i++) {
                    console.log("111");
                    if (search_tag[i].indexOf(query) !== -1) {
                        element.style.display = default_display_property;
                    }
                }
            });
        }, false);
    }

    focus() {
        const is_search_box_active = document.activeElement === this;
        if (!is_search_box_active) {
            this.text_box.focus();
        }
    }

    blur() {
        const is_search_box_active = document.activeElement === this;
        if (is_search_box_active) {
            this.text_box.blur();
        }
    }

    normalize_text(text) {
        return text.toLowerCase().normalize("NFKC").replace(/[\u3041-\u3096]/g, (match) => {
            var result = match.charCodeAt(0) + 0x60;
            return String.fromCharCode(result);
        });
    }

    change_text_box_value(value) {
        this.text_box.value = value;
        this.text_box.dispatchEvent(new Event("input"));
        if (value) {
            this.clear_icon_outer.style.display = "inline-block";
            this.text_box_outer.style.width = this.text_box_outer_width.entered;
        } else {
            this.clear_icon_outer.style.display = "none";
            this.text_box_outer.style.width = this.text_box_outer_width.not_entered;
        }
    }

    static get observedAttributes() {
        return ["value"];
    }

    attributeChangedCallback(name, old_value, new_value) {
        switch (name) {
            case "value":
                this.change_text_box_value(new_value);
                break;
        }
    }

    get value() {
        return this.text_box.value;
    }

    set value(value) {
        this.text_box.setAttribute("value", value);
    }
}

customElements.define("search-box", SearchBox);

javascript
document.addEventListener("DOMContentLoaded", () => {

    initializeLoader();

    initializeBackToTop();

    initializeNavbar();

    initializeFlashMessages();

    initializeTooltips();

    initializeToasts();

    initializeSmoothScroll();

    initializeClipboard();

    initializeDeleteConfirmation();

    initializePasswordToggles();

    initializeQuantityControls();

    initializeImagePreview();

});

function initializeLoader() {

    const loader = document.getElementById("loader");

    if (!loader) return;

    window.addEventListener("load", () => {

        loader.classList.add("hide");

        setTimeout(() => {

            loader.remove();

        }, 400);

    });

}

function initializeNavbar() {

    const navbar = document.querySelector(".navbar");

    if (!navbar) return;

    window.addEventListener("scroll", () => {

        if (window.scrollY > 30) {

            navbar.classList.add("shadow");

        } else {

            navbar.classList.remove("shadow");

        }

    });

}

function initializeBackToTop() {

    const button = document.getElementById("backToTop");

    if (!button) return;

    window.addEventListener("scroll", () => {

        if (window.scrollY > 300) {

            button.style.display = "flex";

        } else {

            button.style.display = "none";

        }

    });

    button.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}

function initializeSmoothScroll() {

    document.querySelectorAll('a[href^="#"]')

        .forEach(link => {

            link.addEventListener("click", event => {

                const target = document.querySelector(

                    link.getAttribute("href")

                );

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({

                    behavior: "smooth",

                    block: "start"

                });

            });

        });

}

function initializeFlashMessages() {

    document.querySelectorAll(".alert")

        .forEach(alert => {

            setTimeout(() => {

                bootstrap.Alert

                    .getOrCreateInstance(alert)

                    .close();

            }, 5000);

        });

}

function initializeTooltips() {

    document.querySelectorAll(

        '[data-bs-toggle="tooltip"]'

    ).forEach(element => {

        new bootstrap.Tooltip(element);

    });

}

function initializeToasts() {

    document.querySelectorAll(".toast")

        .forEach(element => {

            bootstrap.Toast

                .getOrCreateInstance(element)

                .show();

        });

}

function showToast(message, type = "primary") {

    const toast = document.getElementById("liveToast");

    const body = document.getElementById("toastMessage");

    if (!toast || !body) return;

    toast.className = `toast text-bg-${type}`;

    body.innerHTML = message;

    bootstrap.Toast

        .getOrCreateInstance(toast)

        .show();

}

function initializeClipboard() {

    document.querySelectorAll("[data-copy]")

        .forEach(button => {

            button.addEventListener("click", () => {

                navigator.clipboard

                    .writeText(button.dataset.copy)

                    .then(() => {

                        showToast(

                            "Copied to clipboard.",

                            "success"

                        );

                    })

                    .catch(() => {

                        showToast(

                            "Unable to copy.",

                            "danger"

                        );

                    });

            });

        });

}

function initializeDeleteConfirmation() {

    document.querySelectorAll(".delete-confirm")

        .forEach(button => {

            button.addEventListener("click", event => {

                const confirmed = confirm(

                    "Are you sure you want to continue?"

                );

                if (!confirmed) {

                    event.preventDefault();

                }

            });

        });

}

function initializePasswordToggles() {

    document.querySelectorAll(

        "[data-toggle-password]"

    ).forEach(button => {

        const input = document.querySelector(

            button.dataset.togglePassword

        );

        if (!input) return;

        button.addEventListener("click", () => {

            if (input.type === "password") {

                input.type = "text";

                button.innerHTML =

                    '<i class="bi bi-eye-slash"></i>';

            } else {

                input.type = "password";

                button.innerHTML =

                    '<i class="bi bi-eye"></i>';

            }

        });

    });

}

function initializeQuantityControls() {

    document.querySelectorAll(".quantity-input")

        .forEach(input => {

            input.addEventListener("input", () => {

                let value = parseInt(input.value);

                if (isNaN(value) || value < 1) {

                    input.value = 1;

                }

            });

        });

}

function initializeImagePreview() {

    document.querySelectorAll(

        'input[type="file"][data-preview]'

    ).forEach(input => {

        const preview = document.querySelector(

            input.dataset.preview

        );

        if (!preview) return;

        input.addEventListener("change", event => {

            const file = event.target.files[0];

            if (!file) return;

            preview.src = URL.createObjectURL(file);

            preview.classList.remove("d-none");

        });

    });

}

function initializeFormValidation() {

    document.querySelectorAll("form[data-validate]")

        .forEach(form => {

            form.addEventListener("submit", event => {

                let valid = true;

                form.querySelectorAll("[required]")

                    .forEach(field => {

                        if (!field.value.trim()) {

                            valid = false;

                            field.classList.add("is-invalid");

                        } else {

                            field.classList.remove("is-invalid");

                        }

                    });

                if (!valid) {

                    event.preventDefault();

                    showToast(

                        "Please complete all required fields.",

                        "warning"

                    );

                }

            });

        });

}

function initializeSearchFilter() {

    document.querySelectorAll("[data-search]")

        .forEach(input => {

            const target = document.querySelector(

                input.dataset.search

            );

            if (!target) return;

            input.addEventListener("keyup", () => {

                const keyword = input.value

                    .toLowerCase()

                    .trim();

                target.querySelectorAll("[data-filter]")

                    .forEach(item => {

                        const text = item.dataset.filter

                            .toLowerCase();

                        item.style.display =

                            text.includes(keyword)

                            ? ""

                            : "none";

                    });

            });

        });

}

function initializeAutoSubmit() {

    document.querySelectorAll("[data-auto-submit]")

        .forEach(element => {

            element.addEventListener("change", () => {

                const form = element.closest("form");

                if (form) {

                    form.submit();

                }

            });

        });

}

function initializeLoadingButtons() {

    document.querySelectorAll("form")

        .forEach(form => {

            form.addEventListener("submit", () => {

                const button = form.querySelector(

                    '[type="submit"]'

                );

                if (!button) return;

                button.dataset.original =

                    button.innerHTML;

                button.disabled = true;

                button.innerHTML =

                    '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';

            });

        });

}

function initializeCharacterCounters() {

    document.querySelectorAll("[data-counter]")

        .forEach(input => {

            const output = document.querySelector(

                input.dataset.counter

            );

            if (!output) return;

            const update = () => {

                output.textContent = input.value.length;

            };

            update();

            input.addEventListener(

                "input",

                update

            );

        });

}

function initializeNumberFormatting() {

    document.querySelectorAll(".number-format")

        .forEach(element => {

            const value = parseFloat(

                element.textContent

            );

            if (isNaN(value)) return;

            element.textContent =

                value.toLocaleString();

        });

}

function initializeCurrencyFormatting() {

    document.querySelectorAll(".currency")

        .forEach(element => {

            const value = parseFloat(

                element.dataset.value

            );

            if (isNaN(value)) return;

            element.textContent =

                formatCurrency(value);

        });

}

function initializeInputSanitizer() {

    document.querySelectorAll("[data-trim]")

        .forEach(input => {

            input.addEventListener("blur", () => {

                input.value =

                    input.value.trim();

            });

        });

}

function initializeLazyImages() {

    const images = document.querySelectorAll(

        "img[data-src]"

    );

    if (!("IntersectionObserver" in window)) {

        images.forEach(image => {

            image.src = image.dataset.src;

        });

        return;

    }

    const observer = new IntersectionObserver(

        entries => {

            entries.forEach(entry => {

                if (!entry.isIntersecting)

                    return;

                const image = entry.target;

                image.src = image.dataset.src;

                image.removeAttribute(

                    "data-src"

                );

                observer.unobserve(image);

            });

        }

    );

    images.forEach(image => {

        observer.observe(image);

    });

}

async function request(

    url,

    options = {}

) {

    const response = await fetch(

        url,

        options

    );

    if (!response.ok) {

        throw new Error(

            "Request failed."

        );

    }

    const type = response.headers.get(

        "content-type"

    );

    if (

        type &&

        type.includes(

            "application/json"

        )

    ) {

        return response.json();

    }

    return response.text();

}

function get(url) {

    return request(url);

}

function post(

    url,

    data

) {

    return request(

        url,

        {

            method: "POST",

            body: data

        }

    );

}

initializeFormValidation();

initializeSearchFilter();

initializeAutoSubmit();

initializeLoadingButtons();

initializeCharacterCounters();

initializeNumberFormatting();

initializeCurrencyFormatting();

initializeInputSanitizer();

initializeLazyImages();

function saveToStorage(key, value) {

    localStorage.setItem(

        key,

        JSON.stringify(value)

    );

}

function getFromStorage(key, fallback = null) {

    const value = localStorage.getItem(key);

    if (!value) {

        return fallback;

    }

    try {

        return JSON.parse(value);

    } catch {

        return fallback;

    }

}

function removeFromStorage(key) {

    localStorage.removeItem(key);

}

function clearStorage() {

    localStorage.clear();

}

function saveToSession(key, value) {

    sessionStorage.setItem(

        key,

        JSON.stringify(value)

    );

}

function getFromSession(key, fallback = null) {

    const value = sessionStorage.getItem(key);

    if (!value) {

        return fallback;

    }

    try {

        return JSON.parse(value);

    } catch {

        return fallback;

    }

}

function debounce(callback, delay = 300) {

    let timer;

    return (...args) => {

        clearTimeout(timer);

        timer = setTimeout(() => {

            callback(...args);

        }, delay);

    };

}

function throttle(callback, delay = 300) {

    let waiting = false;

    return (...args) => {

        if (waiting) return;

        callback(...args);

        waiting = true;

        setTimeout(() => {

            waiting = false;

        }, delay);

    };

}

function openModal(id) {

    const element = document.getElementById(id);

    if (!element) return;

    bootstrap.Modal

        .getOrCreateInstance(element)

        .show();

}

function closeModal(id) {

    const element = document.getElementById(id);

    if (!element) return;

    bootstrap.Modal

        .getOrCreateInstance(element)

        .hide();

}

function formatDate(date) {

    return new Date(date)

        .toLocaleDateString(

            "en-KE",

            {

                year: "numeric",

                month: "long",

                day: "numeric"

            }

        );

}

function formatDateTime(date) {

    return new Date(date)

        .toLocaleString(

            "en-KE"

        );

}

function randomId(length = 10) {

    const chars =

        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    let result = "";

    for (

        let i = 0;

        i < length;

        i++

    ) {

        result += chars.charAt(

            Math.floor(

                Math.random() * chars.length

            )

        );

    }

    return result;

}

function uuid() {

    return crypto.randomUUID();

}

function downloadFile(filename, content) {

    const blob = new Blob(

        [content],

        {

            type: "text/plain"

        }

    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(url);

}

function printPage() {

    window.print();

}

function getQueryParameter(name) {

    return new URLSearchParams(

        window.location.search

    ).get(name);

}

function setQueryParameter(name, value) {

    const url = new URL(

        window.location

    );

    url.searchParams.set(

        name,

        value

    );

    window.history.replaceState(

        {},

        "",

        url

    );

}

window.showToast = showToast;

window.formatCurrency = formatCurrency;

window.copyToClipboard = copyToClipboard;

window.saveToStorage = saveToStorage;

window.getFromStorage = getFromStorage;

window.removeFromStorage = removeFromStorage;

window.saveToSession = saveToSession;

window.getFromSession = getFromSession;

window.debounce = debounce;

window.throttle = throttle;

window.openModal = openModal;

window.closeModal = closeModal;

window.formatDate = formatDate;

window.formatDateTime = formatDateTime;

window.randomId = randomId;

window.uuid = uuid;

window.downloadFile = downloadFile;

window.printPage = printPage;

window.getQueryParameter = getQueryParameter;

window.setQueryParameter = setQueryParameter;

window.get = get;

window.post = post;


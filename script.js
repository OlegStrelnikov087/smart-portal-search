'use strict';
const GLOBAL_WRAPPER = document.getElementById("main-wrapper");
const USER_PROMPT = document.getElementById("user-prompt");
const MAIN_BUTTON = document.getElementById("set-query");
const HELP_MESSAGES_WRAPPER = document.getElementById("help-messages-wrapper");

let isBottom=false;
let isDisabled=false;
class ModalWindow {
    constructor() {
        this.modal=null;
    }
    static openModal(availableWindow) {
        if(this.modal) {return;}
        const open = () => {
            this.modal = document.createElement("div");
            this.modal.className = "modal";
            if (availableWindow)
            this.modal.append(availableWindow);
            document.body.append(this.modal);
            setTimeout(() => {
                this.modal.style.opacity=1;
            }, 10);
        };
        if(HelpMessages.pastElem) {
            interfaceToCenter();
            HelpMessages.removePastElement(open);
        }
        else open();
    }
    static closeModal() {
        if(!this.modal) return;
        this.modal.addEventListener("transitionend", event=>{
            if(event.target!==this.modal || event.propertyName!=="opacity") return;
            this.modal.remove();
            this.modal=null;
        });
        this.modal.style.opacity=0;
    }
}
function toggleStatusElements(status) {
    if(status) isDisabled=status;
    else isDisabled=!isDisabled;
    MAIN_BUTTON.disabled=isDisabled;
    MAIN_BUTTON.style.pointerEvents=(isDisabled) ? 'none' : '';
    
    USER_PROMPT.disabled=isDisabled;
    USER_PROMPT.readOnly=isDisabled;
    USER_PROMPT.style.pointerEvents=(isDisabled) ? 'none' : '';
}

async function enterRequest() {
    if(isDisabled) return;
    const message = USER_PROMPT.value.trim();
    if(!message.match(/.*[a-zA-Zа-яА-Я].*/)) return;
    interfaceToBottom();
    toggleStatusElements(true);
    HelpMessages.setHelpMessage(message, () => toggleStatusElements(false));
};

MAIN_BUTTON.addEventListener("pointerdown", event => {
    if (event.button !== 0) return;
    enterRequest();
});
document.addEventListener("keydown", event=>{
    if(event.key==="Enter") enterRequest();
});

function interfaceToBottom() {
    if(isBottom) return;
    const startUP = USER_PROMPT.getBoundingClientRect().bottom-10-USER_PROMPT.offsetHeight;
    APIMethods.animate({
        timing: value=>value,
        draw: progress=>{
            USER_PROMPT.style.bottom=-progress*startUP+'px';
        },
        duration: 250
    });
    const startMB = MAIN_BUTTON.getBoundingClientRect().bottom-(USER_PROMPT.offsetHeight-MAIN_BUTTON.offsetHeight)-MAIN_BUTTON.offsetHeight;
    APIMethods.animate({
        timing: value=>value,
        draw: progress=> {
            MAIN_BUTTON.style.bottom=-progress*startMB+'px';
        },
        duration:250
    });
    isBottom=true;
}

function interfaceToCenter() {
    if(!isBottom) return;
    const startUP = +getComputedStyle(USER_PROMPT).bottom.slice(0, -2);
    const startMB = +getComputedStyle(MAIN_BUTTON).bottom.slice(0,-2);
    APIMethods.animate({
        timing: value=>value,
        draw: progress=>{
            USER_PROMPT.style.bottom=(1-progress)*startUP+'px';
        },
        duration: 250
    });
    APIMethods.animate({
        timing: value=>value,
        draw: progress=> {
            MAIN_BUTTON.style.bottom=(1-progress)*startMB+'px';
        },
        duration:250
    });
    isBottom=false;
}

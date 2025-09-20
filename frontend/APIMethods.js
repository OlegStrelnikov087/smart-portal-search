class APIMethods {
    static createBuyingForm(header = "Закупка") {
        const buyingForm = document.createElement("div");
        buyingForm.className = "buying-form";
        const headerText = document.createElement("h1");
        headerText.textContent = header;
        buyingForm.append(headerText);
        const closeButton = document.createElement("button");
        closeButton.className="close-icon-button";
        closeButton.addEventListener("pointerdown", event=>{
            if(event.button!==0) return;
            buyingForm.style.opacity=0;
            ModalWindow.closeModal();
            closeButton.disabled=true;
        });
        buyingForm.append(closeButton);
        return buyingForm;
    }
    static animate({timing, draw, duration, afterEndCallback}) {
        const start = performance.now();
        requestAnimationFrame(function animation(time) {
            const timeFraction = Math.min(1, ((time-start)/duration));
            const progress = timing(timeFraction);
            draw(progress);
            if(timeFraction<1) requestAnimationFrame(animation);
            else {
                if(afterEndCallback) afterEndCallback();
            }
        });
    }
    
    
}
class HelpMessages {
    constructor() {
        this.pastElem=null;
    }
    static setHelpMessage(message, callback) {
        const helpMessage = document.createElement("div");
        const TOP_OFFSET=5;
        helpMessage.className="help-message";
        if(this.pastElem) {
            this.removePastElement(() => addNewBlock.call(this));
        }
        else addNewBlock.call(this);
        const once = event=>{
            if(event.propertyName!=="left") return;
            APIMethods.animate({
                timing: value=>value,
                draw: progress => {
                    const messageChunk = message.slice(0, message.length*progress);
                    helpMessage.textContent=messageChunk;
                },
                duration: message.length*20,
                afterEndCallback: () => {
                    if(callback) callback();
                }
            });
            helpMessage.removeEventListener("transitionend", once);
        };
        helpMessage.addEventListener("transitionend", once);
        function addNewBlock() {
            helpMessage.style.top=TOP_OFFSET+'px';
             HELP_MESSAGES_WRAPPER.append(helpMessage);
             setTimeout(() => {
                helpMessage.style.left="50%";
                helpMessage.style.transform="translateX(-50%)"; 
            }, 10);
            this.pastElem=helpMessage;
        }
    }
    static removePastElement(callback) {
        this.pastElem.style.left="-100%";
        this.pastElem.addEventListener("transitionend", event=>{
            if(event.propertyName!=="left") return;
            this.pastElem.remove();
            this.pastElem=null;
            callback();
        });
    }
}
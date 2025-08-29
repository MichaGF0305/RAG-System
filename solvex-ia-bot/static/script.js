document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");

    // Función para añadir mensajes al chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", `${sender}-message`);
        
        const p = document.createElement("p");
        p.textContent = text;
        messageDiv.appendChild(p);
        
        chatContainer.appendChild(messageDiv);
        // Hacer scroll automático al final
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return messageDiv;
    }

    // Manejar el envío del formulario
    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const userText = userInput.value.trim();
        if (!userText) return;

        // Añadir el mensaje del usuario y limpiar el input
        addMessage(userText, "user");
        userInput.value = "";

        // Mostrar un mensaje de "pensando..."
        const loadingMessage = addMessage("...", "bot");
        loadingMessage.classList.add("loading");

        try {
            // Enviar la pregunta a la API
            const response = await fetch("/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: "web-ui-user", // ID de usuario genérico
                    query: userText,
                }),
            });

            if (!response.ok) {
                throw new Error("El servidor respondió con un error.");
            }

            const data = await response.json();
            
            // Actualizar el mensaje de "pensando" con la respuesta real
            loadingMessage.querySelector("p").textContent = data.answer;
            loadingMessage.classList.remove("loading");

        } catch (error) {
            console.error("Error al contactar la API:", error);
            loadingMessage.querySelector("p").textContent = "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.";
            loadingMessage.classList.remove("loading");
        } finally {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });
});
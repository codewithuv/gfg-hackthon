import re


qa_pairs = {
    "hello": "Hi there! How can I help you today?",
    "what is your name": "I am a chatbot created to assist you. You can call me Chatbot.",
    "how are you": "I'm just a program, but I'm here to help you!",
    "what can you do": "I can help you determine whether you might have diabetes based on some questions or calculate your BMI.",
    "bye": "Goodbye! Have a great day!",
    "bmi": "To calculate your BMI, I need your weight and height. What is your weight in kilograms?",
    "gender": "Please tell me your gender (e.g., gender = female).",
    "pregnancy": "Are you pregnant?",
    "family history": "Do you have a family history of diabetes?",
    "frequent urination": "Do you experience frequent urination?",
    "excessive thirst": "Do you experience excessive thirst?",
    "tiredness": "Do you feel very tired frequently?",
    "blurred vision": "Do you have blurred vision?",
    "age": "What is your age?",
    "high blood pressure": "Do you have high blood pressure?",
    "unhealthy diet": "Do you have an unhealthy diet?",
    "exercise": "Do you exercise regularly?",
    "weight": "What is your weight in kilograms?",
    "height": "What is your height in centimeters?",
    "info": "Do you want to know more about diabetes?",
}


questions = [
    "Are you pregnant?",
    "Do you have a family history of diabetes?",
    "Do you experience frequent urination?",
    "Do you experience excessive thirst?",
    "Do you feel very tired frequently?",
    "Do you have blurred vision?",
    "What is your age?",
    "Do you have high blood pressure?",
    "Do you have an unhealthy diet?",
    "Do you exercise regularly?",
    "What is your weight in kilograms?",
    "What is your height in centimeters?",
    "Do you want to know more about diabetes?"  
]


diabetes_info = (
    "Diabetes is a chronic condition that affects how your body turns food into energy. "
    "With diabetes, your body either doesn’t make enough insulin or can’t use its insulin as well as it should. "
    "Insulin is a hormone that helps regulate blood sugar levels. There are two main types of diabetes: Type 1 and Type 2. "
    "Type 1 diabetes is usually diagnosed in children and young adults, where the body does not produce insulin. "
    "Type 2 diabetes is more common and is usually diagnosed in adults; in this type, the body is unable to use insulin effectively. "
    "Managing diabetes involves monitoring blood sugar levels, maintaining a healthy diet, exercising regularly, and following prescribed medications."
)

def calculate_bmi(weight, height):
    
    height_m = height / 100
   
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_response(user_input, state):
    
    user_input = user_input.lower().strip()

    print("User Input:", user_input)  
    print("Current State:", state)  

    
    if "bmi" in user_input:
        state['step'] = 'ask_weight_height'
        return "To calculate your BMI, I need your weight and height. What is your weight in kilograms?"

    
    if state['step'] == 'ask_weight_height':
        if state['weight'] is None:
            try:
                state['weight'] = float(user_input)
                return "Thank you. Now, please provide your height in centimeters."
            except ValueError:
                return "Please enter a valid number for your weight."
        
        if state['height'] is None:
            try:
                state['height'] = float(user_input)
                
                bmi = calculate_bmi(state['weight'], state['height'])
                state['weight'] = None
                state['height'] = None  
                state['step'] = 'post_bmi'  
                return f"Your BMI is {bmi}. Is there anything else I can assist you with? Type 'yes' to continue with diabetes-related questions or 'no' to exit."
            except ValueError:
                return "Please enter a valid number for your height."

    
    if state['step'] == 'post_bmi':
        if 'yes' in user_input:
            state['step'] = 'ask_diabetes'  
            state['step_index'] = 0
            return "Great! Let's start with some questions to assess your diabetes risk."
        else:
            state['step'] = 'final_question'
            return "Is there anything else I can assist you with?"

    
    if state['step'] == 'ask_diabetes':
        if state['gender'] == 'female':
            if state['step_index'] == 0:
                state['step_index'] += 1
                return questions[0]  
            else:
                # Proceed with the remaining questions
                if state['step_index'] < len(questions) - 2:  
                    state['step_index'] += 1
                    return questions[state['step_index']]
                else:
                    state['step'] = 'final_question'
                    return "Okay, I got this. Redirecting to our main servers."
        
        elif state['gender'] == 'male':
            if state['step_index'] == 0:
                state['step_index'] += 1  
            if state['step_index'] < len(questions) - 2:  
                state['step_index'] += 1
                return questions[state['step_index']]
            else:
                state['step'] = 'final_question'
                return "Okay, I got this. Redirecting to our main servers."

    
    if state['step'] == 0:
        if "gender" in user_input:
            state['gender'] = re.findall(r'gender\s*=\s*(\w+)', user_input)[0]
            state['step'] = 'ask_diabetes'
            state['step_index'] = 0
            return "Great, let's start with some questions to assess your diabetes risk."
        else:
            return "Please provide your gender in the format: gender = female."

    if state['step'] == 'final_question':
        if 'yes' in user_input:
            return diabetes_info
        else:
            return "Okay, I got this. Redirecting to our main servers."

    return "I'm sorry, I don't understand that question."

def chat():
    print("Welcome to the Chatbot! Type 'bye' to exit.")
    state = {
        'step': 0,  # Start at the initial question
        'responses': [],  # Store user responses
        'weight': None,
        'height': None,
        'gender': None,
        'pregnant': None,
        'step_index': 0  # Track the current question index
    }
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        response = get_response(user_input, state)
        
        print("Chatbot:", response)
        
        # Exit the loop if the final response is given
        if state['step'] == 'final_question' and 'yes' in user_input:
            break

if __name__ == "__main__":
    chat()

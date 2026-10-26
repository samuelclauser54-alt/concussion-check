import streamlit as st
import time
import random
st.set_page_config(page_title="Concussion Check",
                   page_icon=":material/sports:")

st.title("Concussion Check")

st.caption("Sideline screen for coaches, not a diagnosis")

SYMPTOMS = [
    "Headache", "Pressure in head", "Neck pain", "Nausea",
    "Dizziness", "Blurred vision", "Balance problems", "Sensitivity to light",
    "Sensitivity to noise", "Feeling slowed down",
    "Don't feel right",  "Difficulty remembering",
    "Confusion", "Irritability",
    "Nervous or anxious"
]


DANGER_SIGNS = [
    "Neck pain or tenderness", "Seizure or convulsion", "Lost consciousness (knocked out)",
    "Severe or worsening headache", "Double vision",
    "Weakness, tingling, or burning in arms or legs",
    "Getting more drowsy or harder to wake up", "Combative behavior",
    "Vomiting"
]
OBSERVABLE_SIGNS = [
    "Lying motionless on the ground", "Slow to get up after a hit",
    "Stumbling or trouble walking", "Confused or can't answer questions",
    "Blank or vacant look", "Facial injury after a hit to the head",
]


def symptom_points(severity):
    if severity == 0:
        return 0
    elif severity <= 3:
        return 2
    elif severity <= 10:
        return 4
    else:
        return 6


danger_signs = 0

st.header(":red[:material/warning:] Danger Signs")

with st.container(border=True):

    for danger in (DANGER_SIGNS):
        checked = st.checkbox(danger)
        if checked:
            danger_signs = danger_signs + 1
        else:
            danger_signs = danger_signs + 0
if danger_signs > 0:
    st.error("EMERGENCY: Call 911 now")
    st.write(
        "Do not move them if they have neck pain, stay with them, no food or drink.")
    st.stop()

observed = 0

with st.container(border=True):
    st.header(":material/visibility: Observable Signs")
    for observable in (OBSERVABLE_SIGNS):
        positive = st.checkbox(observable)
        if positive:
            observed = observed + 1
        else:
            observed = observed + 0


total = 0

with st.container(border=True):
    st.header(":material/sick: Symptoms")
    for symptom in SYMPTOMS:
        value = st.slider(symptom, 0, 6, 0)
        total = total + value


def severity(total):
    if total == 0:
        return ("None")
    elif total <= 3:
        return ("Mild")
    elif total <= 10:
        return ("Moderate")
    else:
        return ("High")


st.write("Severity: ", severity(total))

WORD_LISTS = [
    ["Pencil", "Rabbit", "Orange", "Bridge", "Cloud"],
    ["Ladder", "Turtle", "Cheese", "Forest", "Bucket"],
    ["Hammer", "Parrot", "Cookie", "Garden", "Thunder"],
    ["Kettle", "Zebra", "Pickle", "Castle", "River"],
]

if "words" not in st.session_state:
    st.session_state.words = random.choice(WORD_LISTS)
WORDS = st.session_state.words
memory = 0


# Memory Test


if "memory_phase" not in st.session_state:
    st.session_state.memory_phase = "start"
st.header(":material/psychology: Memory")
if st.session_state.memory_phase == "start":
    st.write("5 words will appear for 10 seconds. Try to remember them.")
    if st.button("Show words"):
        st.session_state.memory_phase = "showing"
        st.rerun()


elif st.session_state.memory_phase == "showing":
    st.subheader("    ".join(WORDS))
    time.sleep(10)
    st.session_state.memory_phase = "recall"
    st.rerun()

elif st.session_state.memory_phase == "recall":
    answer = st.text_input("Type the words you remember (any order):")
    typed = answer.lower().replace(",", " ").split()
    with st.container(border=True):
        for word in WORDS:
            if word.lower() in typed:
                memory = memory + 1
    st.write("You remember", memory, "of 5")

QUESTIONS = [
    "What month is it?", "What is the date today?",
    "What day of the week is it?",
    "What year is it?", "About what time is it?"
]

st.header(":material/explore: Orientation")
st.write("Ask or answer each question, tick if answered correctly")
orientation = 0
with st.container(border=True):
    for question in QUESTIONS:
        if st.checkbox(question):
            orientation = orientation + 1


def memory_points(memory):
    if memory >= 4:
        return 0
    elif memory == 3:
        return 1
    elif memory == 2:
        return 2
    else:
        return 3


def orientation_points(orientation):
    if orientation == 5:
        return 0
    elif orientation == 4:
        return 1
    else:
        return 3


st.header(":material/assignment: Result")
points = symptom_points(total) + memory_points(memory) + \
    orientation_points(orientation) + 3 * observed
st.metric("Concern score", points)
if points == 0:
    st.success(
        "No signs found. NOT cleared: re-check in 15 minutes and tonight. If in doubt, sit out. ")
elif points <= 3:
    st.warning(
        "Possible concussion. Sit out the rest of today, re-check symptoms and tell a parent or guardian. ")
elif points <= 7:
    st.error(
        "Likely concussion. Out for today. See a doctor within 24 hours. Tell a parent. ")
else:
    st.error(
        "Strong signs of concussion. See a doctor today and watch closely for danger signs. ")

import * as React from "react";
import { View, StyleSheet, ScrollView } from "react-native";
import { Provider as PaperProvider, Text, Button, TextInput } from "react-native-paper";
import { NavigationContainer } from "@react-navigation/native";
import { createDrawerNavigator } from "@react-navigation/drawer";

const Drawer = createDrawerNavigator();

// --- Dashboard Screen ---
function DashboardScreen() {
  return (
    <View style={styles.center}>
      <Text style={styles.title}>📊 Dashboard</Text>
    </View>
  );
}

// --- Reports Screen ---
function ReportsScreen() {
  return (
    <View style={styles.center}>
      <Text style={styles.title}>📝 Reports Submission</Text>
    </View>
  );
}

// --- Water Quality & Health Checker ---
function WaterQualityScreen() {
  const [ph, setPh] = React.useState("");
  const [tds, setTds] = React.useState("");
  const [turbidity, setTurbidity] = React.useState("");
  const [symptoms, setSymptoms] = React.useState("");
  const [result, setResult] = React.useState("");

  const diseaseRules = {
    "Cholera": ["diarrhea", "dehydration", "vomiting"],
    "Typhoid": ["fever", "abdominal pain", "headache"],
    "Hepatitis A": ["jaundice", "fatigue", "loss of appetite"],
    "Giardiasis": ["diarrhea", "stomach cramps", "bloating"],
    "Dysentery": ["bloody diarrhea", "abdominal pain", "fever"],
    "E. coli Infection": ["stomach cramps", "diarrhea", "nausea"],
  };

  const predict = () => {
    // Fake Water Quality Logic (you can replace with backend ML API)
    let waterResult = parseFloat(ph) >= 6.5 && parseFloat(ph) <= 8.5 ? "✅ Safe" : "❌ Unsafe";

    // Symptom Check
    let foundDiseases = [];
    const userSymptoms = symptoms.toLowerCase();
    for (let disease in diseaseRules) {
      if (diseaseRules[disease].some(s => userSymptoms.includes(s))) {
        foundDiseases.push(disease);
      }
    }
    if (foundDiseases.length === 0) {
      foundDiseases.push("No match. Consult a doctor.");
    }

    setResult(`💧 Water Quality: ${waterResult}\n🩺 Possible Diseases: ${foundDiseases.join(", ")}`);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>💧 Water & Health Checker 💧</Text>
      <TextInput label="pH (e.g., 7.2)" value={ph} onChangeText={setPh} style={styles.input} mode="outlined" />
      <TextInput label="TDS mg/L (e.g., 307)" value={tds} onChangeText={setTds} style={styles.input} mode="outlined" />
      <TextInput label="Turbidity NTU (e.g., 1.3)" value={turbidity} onChangeText={setTurbidity} style={styles.input} mode="outlined" />
      <TextInput
        label="Symptoms (e.g., fever, diarrhea)"
        value={symptoms}
        onChangeText={setSymptoms}
        style={styles.input}
        mode="outlined"
        multiline
      />
      <Button mode="contained" onPress={predict} style={styles.button}>
        Check Health & Water Safety
      </Button>
      {result !== "" && <Text style={styles.result}>{result}</Text>}
    </ScrollView>
  );
}

// --- Alerts Screen ---
function AlertsScreen() {
  return (
    <View style={styles.center}>
      <Text style={styles.title}>🚨 Alerts & Notifications</Text>
    </View>
  );
}

// --- Resources Screen ---
function ResourcesScreen() {
  return (
    <View style={styles.center}>
      <Text style={styles.title}>📚 Resources & Awareness</Text>
    </View>
  );
}

// --- Settings Screen ---
function SettingsScreen() {
  return (
    <View style={styles.center}>
      <Text style={styles.title}>⚙️ Settings</Text>
    </View>
  );
}

// --- Main App ---
export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Drawer.Navigator initialRouteName="Dashboard">
          <Drawer.Screen name="Dashboard" component={DashboardScreen} />
          <Drawer.Screen name="Reports Submission" component={ReportsScreen} />
          <Drawer.Screen name="Water Quality" component={WaterQualityScreen} />
          <Drawer.Screen name="Alerts & Notifications" component={AlertsScreen} />
          <Drawer.Screen name="Resources & Awareness" component={ResourcesScreen} />
          <Drawer.Screen name="Settings" component={SettingsScreen} />
        </Drawer.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}

// --- Styles ---
const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: "#F4F8FF",
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F4F8FF",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: "#003366",
  },
  input: {
    marginBottom: 15,
    backgroundColor: "white",
  },
  button: {
    marginTop: 10,
    padding: 5,
  },
  result: {
    marginTop: 20,
    fontSize: 16,
    textAlign: "center",
    color: "#222",
  },
});

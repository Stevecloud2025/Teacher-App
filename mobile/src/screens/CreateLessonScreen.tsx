import React, { useState } from 'react';
import {
ActivityIndicator,
Alert,
KeyboardAvoidingView,
Platform,
ScrollView,
StyleSheet,
Text,
TextInput,
TouchableOpacity,
View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as SecureStore from 'expo-secure-store';
import {
createTeacherLesson,
CreateLessonData,
} from '../api';

type CreateLessonScreenProps = {
onBack: () => void;
onLessonCreated: () => void;
};

export default function CreateLessonScreen({
onBack,
onLessonCreated,
}: CreateLessonScreenProps) {
const [title, setTitle] = useState('');
const [subject, setSubject] = useState('');
const [className, setClassName] = useState('');
const [topic, setTopic] = useState('');
const [content, setContent] = useState('');
const [saving, setSaving] = useState(false);

const handleSave = async () => {
if (
!title.trim() ||
!subject.trim() ||
!className.trim() ||
!topic.trim() ||
!content.trim()
) {
Alert.alert(
'Incomplete Lesson',
'Please fill in all fields before saving.',
);
return;
}

try {
  setSaving(true);

  const accessToken = await SecureStore.getItemAsync(
    'teacher_app_access_token',
  );

  if (!accessToken) {
    throw new Error('Your session has expired. Please log in again.');
  }

  const lessonData: CreateLessonData = {
    title: title.trim(),
    subject: subject.trim(),
    class_name: className.trim(),
    topic: topic.trim(),
    content: content.trim(),
    status: 'draft',
  };

  await createTeacherLesson(accessToken, lessonData);

  Alert.alert(
    'Lesson Saved',
    'Your lesson has been saved as a draft.',
    [
      {
        text: 'OK',
        onPress: onLessonCreated,
      },
    ],
  );
} catch (error) {
  Alert.alert(
    'Unable to Save Lesson',
    error instanceof Error
      ? error.message
      : 'An unexpected error occurred.',
  );
} finally {
  setSaving(false);
}


};

return ( <SafeAreaView style={styles.container}>
<KeyboardAvoidingView
style={styles.flex}
behavior={Platform.OS === 'ios' ? 'padding' : undefined}
> <View style={styles.header}> <TouchableOpacity
         onPress={onBack}
         disabled={saving}
         style={styles.backButton}
       > <Text style={styles.backButtonText}>
{'<- Back'} </Text> </TouchableOpacity>

```
      <Text style={styles.heading}>Create Lesson</Text>
      <Text style={styles.subtitle}>
        Prepare and save your lesson note.
      </Text>
    </View>

    <ScrollView
      keyboardShouldPersistTaps="handled"
      contentContainerStyle={styles.form}
    >
      <Text style={styles.label}>Lesson Title</Text>
      <TextInput
        style={styles.input}
        value={title}
        onChangeText={setTitle}
        placeholder="e.g. Introduction to Fractions"
        placeholderTextColor="#94A3B8"
      />

      <Text style={styles.label}>Subject</Text>
      <TextInput
        style={styles.input}
        value={subject}
        onChangeText={setSubject}
        placeholder="e.g. Mathematics"
        placeholderTextColor="#94A3B8"
      />

      <Text style={styles.label}>Class</Text>
      <TextInput
        style={styles.input}
        value={className}
        onChangeText={setClassName}
        placeholder="e.g. Primary 4"
        placeholderTextColor="#94A3B8"
      />

      <Text style={styles.label}>Topic</Text>
      <TextInput
        style={styles.input}
        value={topic}
        onChangeText={setTopic}
        placeholder="Enter the lesson topic"
        placeholderTextColor="#94A3B8"
      />

      <Text style={styles.label}>Lesson Content</Text>
      <TextInput
        style={[styles.input, styles.contentInput]}
        value={content}
        onChangeText={setContent}
        placeholder="Write your lesson note here..."
        placeholderTextColor="#94A3B8"
        multiline
        textAlignVertical="top"
      />

      <TouchableOpacity
        style={[
          styles.saveButton,
          saving && styles.disabledButton,
        ]}
        onPress={handleSave}
        disabled={saving}
      >
        {saving ? (
          <ActivityIndicator color="#FFFFFF" />
        ) : (
          <Text style={styles.saveButtonText}>
            Save as Draft
          </Text>
        )}
      </TouchableOpacity>
    </ScrollView>
  </KeyboardAvoidingView>
</SafeAreaView>


);
}

const styles = StyleSheet.create({
container: {
flex: 1,
backgroundColor: '#F8FAFC',
},
flex: {
flex: 1,
},
header: {
paddingHorizontal: 18,
paddingTop: 12,
paddingBottom: 16,
},
backButton: {
alignSelf: 'flex-start',
paddingVertical: 8,
marginBottom: 10,
},
backButtonText: {
color: '#2563EB',
fontSize: 16,
fontWeight: '500',
},
heading: {
fontSize: 26,
fontWeight: '700',
color: '#0F172A',
},
subtitle: {
fontSize: 14,
color: '#64748B',
marginTop: 5,
},
form: {
paddingHorizontal: 18,
paddingBottom: 32,
},
label: {
fontSize: 14,
fontWeight: '600',
color: '#334155',
marginBottom: 7,
marginTop: 12,
},
input: {
backgroundColor: '#FFFFFF',
borderWidth: 1,
borderColor: '#CBD5E1',
borderRadius: 10,
paddingHorizontal: 14,
paddingVertical: 12,
fontSize: 15,
color: '#0F172A',
},
contentInput: {
minHeight: 180,
paddingTop: 14,
},
saveButton: {
backgroundColor: '#2563EB',
borderRadius: 10,
paddingVertical: 15,
alignItems: 'center',
justifyContent: 'center',
marginTop: 24,
},
disabledButton: {
opacity: 0.65,
},
saveButtonText: {
color: '#FFFFFF',
fontSize: 16,
fontWeight: '700',
},
});

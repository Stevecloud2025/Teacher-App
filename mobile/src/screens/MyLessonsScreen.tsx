import React, { useCallback, useEffect, useState } from 'react';
import {
ActivityIndicator,
FlatList,
RefreshControl,
StyleSheet,
Text,
TextInput,
TouchableOpacity,
View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as SecureStore from 'expo-secure-store';
import { getTeacherLessons, LessonSummary } from '../api';

type LessonStatus = 'all' | 'draft' | 'published' | 'archived';

type MyLessonsScreenProps = {
  onBack: () => void;
  onCreateLesson: () => void;
};

export default function MyLessonsScreen({
  onBack,
  onCreateLesson,
}: MyLessonsScreenProps) {

const [lessons, setLessons] = useState<LessonSummary[]>([]);
const [search, setSearch] = useState('');
const [status, setStatus] = useState<LessonStatus>('all');
const [loading, setLoading] = useState(true);
const [refreshing, setRefreshing] = useState(false);
const [error, setError] = useState('');

const loadLessons = useCallback(async () => {
try {
setError('');


  const token = await SecureStore.getItemAsync(
    'teacher_app_access_token',
  );

  if (!token) {
    throw new Error(
      'Your session has expired. Please log in again.',
    );
  }

  const response = await getTeacherLessons(token, {
    search: search.trim() || undefined,
    status: status === 'all' ? undefined : status,
  });

  setLessons(response.lessons);
} catch (err) {
  setError(
    err instanceof Error
      ? err.message
      : 'Unable to load your lessons.',
  );
} finally {
  setLoading(false);
  setRefreshing(false);
}


}, [search, status]);

useEffect(() => {
loadLessons();
}, [loadLessons]);

const handleRefresh = () => {
setRefreshing(true);
loadLessons();
};

const renderLesson = ({ item }: { item: LessonSummary }) => ( <View style={styles.lessonCard}> <Text style={styles.lessonTitle}>
{item.title} </Text>

```
  <Text style={styles.lessonDetail}>
    Subject: {item.subject}
  </Text>

  <Text style={styles.lessonDetail}>
    Class: {item.class_name}
  </Text>

  <Text style={styles.lessonDetail}>
    Topic: {item.topic}
  </Text>

  <View style={styles.lessonFooter}>
    <Text
      style={[
        styles.statusBadge,
        item.status === 'published' && styles.publishedBadge,
        item.status === 'archived' && styles.archivedBadge,
      ]}
    >
      {item.status.toUpperCase()}
    </Text>

    <Text style={styles.dateText}>
      Updated:{' '}
      {item.updated_at
        ? new Date(item.updated_at).toLocaleDateString()
        : 'Not available'}
    </Text>
  </View>
</View>


);

if (loading) {
return ( <SafeAreaView style={styles.centered}> <ActivityIndicator
       size="large"
       color="#2563EB"
     /> <Text style={styles.message}>
Loading your lessons... </Text> </SafeAreaView>
);
}

return ( <SafeAreaView style={styles.container}> 
<Text style={styles.heading}>
My Lessons </Text>
<TouchableOpacity
  style={styles.createButton}
  onPress={onCreateLesson}
>
  <Text style={styles.createButtonText}>+ Create Lesson</Text>
</TouchableOpacity>
  <TouchableOpacity
    onPress={onBack}
    style={styles.backButton}
    accessibilityRole="button"
  >
    <Text style={styles.backButtonText}>
      ← Back to Dashboard
    </Text>
  </TouchableOpacity>

  <Text style={styles.subtitle}>
    View and manage your lesson notes.
  </Text>

  <TextInput
    style={styles.searchInput}
    placeholder="Search by title, subject or topic..."
    value={search}
    onChangeText={setSearch}
    autoCapitalize="none"
    returnKeyType="search"
  />

  <View style={styles.filterContainer}>
    {(
      ['all', 'draft', 'published', 'archived'] as LessonStatus[]
    ).map((item) => (
      <TouchableOpacity
        key={item}
        style={[
          styles.filterButton,
          status === item && styles.activeFilterButton,
        ]}
        onPress={() => setStatus(item)}
        accessibilityRole="button"
      >
        <Text
          style={[
            styles.filterText,
            status === item && styles.activeFilterText,
          ]}
        >
          {item === 'all'
            ? 'All'
            : item.charAt(0).toUpperCase() + item.slice(1)}
        </Text>
      </TouchableOpacity>
    ))}
  </View>

  {error ? (
    <View style={styles.errorContainer}>
      <Text style={styles.errorText}>
        {error}
      </Text>

      <TouchableOpacity
        style={styles.retryButton}
        onPress={() => {
          setLoading(true);
          loadLessons();
        }}
        accessibilityRole="button"
      >
        <Text style={styles.retryButtonText}>
          Try Again
        </Text>
      </TouchableOpacity>
    </View>
  ) : (
    <FlatList
      data={lessons}
      keyExtractor={(item) => String(item.id)}
      renderItem={renderLesson}
      contentContainerStyle={
        lessons.length === 0
          ? styles.emptyList
          : styles.listContent
      }
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={handleRefresh}
        />
      }
      ListEmptyComponent={
        <Text style={styles.emptyText}>
          No lessons found. Try another search or filter.
        </Text>
      }
    />
  )}
</SafeAreaView>

);
}

const styles = StyleSheet.create({
container: {
flex: 1,
backgroundColor: '#F8FAFC',
paddingHorizontal: 18,
paddingTop: 18,
},
centered: {
flex: 1,
justifyContent: 'center',
alignItems: 'center',
backgroundColor: '#F8FAFC',
},
heading: {
fontSize: 26,
fontWeight: 'bold',
color: '#0F172A',
},
backButton: {
marginBottom: 15,
},
backButtonText: {
color: '#2563EB',
fontSize: 16,
},
subtitle: {
fontSize: 14,
color: '#64748B',
marginTop: 5,
marginBottom: 18,
},
searchInput: {
backgroundColor: '#FFFFFF',
borderWidth: 1,
borderColor: '#CBD5E1',
borderRadius: 10,
paddingHorizontal: 14,
paddingVertical: 12,
fontSize: 14,
marginBottom: 14,
},
filterContainer: {
flexDirection: 'row',
flexWrap: 'wrap',
gap: 8,
marginBottom: 16,
},
filterButton: {
paddingHorizontal: 13,
paddingVertical: 8,
borderRadius: 20,
backgroundColor: '#E2E8F0',
},
activeFilterButton: {
backgroundColor: '#2563EB',
},
filterText: {
color: '#334155',
fontSize: 12,
fontWeight: '600',
},
activeFilterText: {
color: '#FFFFFF',
},
listContent: {
paddingBottom: 24,
},
emptyList: {
flexGrow: 1,
justifyContent: 'center',
},
lessonCard: {
backgroundColor: '#FFFFFF',
padding: 16,
borderRadius: 12,
marginBottom: 12,
borderWidth: 1,
borderColor: '#E2E8F0',
},
lessonTitle: {
fontSize: 17,
fontWeight: 'bold',
color: '#0F172A',
marginBottom: 10,
},
lessonDetail: {
fontSize: 13,
color: '#475569',
marginBottom: 5,
},
lessonFooter: {
flexDirection: 'row',
justifyContent: 'space-between',
alignItems: 'center',
marginTop: 12,
flexWrap: 'wrap',
gap: 8,
},
statusBadge: {
fontSize: 10,
fontWeight: 'bold',
color: '#92400E',
backgroundColor: '#FEF3C7',
paddingHorizontal: 9,
paddingVertical: 5,
borderRadius: 6,
overflow: 'hidden',
},
publishedBadge: {
color: '#166534',
backgroundColor: '#DCFCE7',
},
archivedBadge: {
color: '#475569',
backgroundColor: '#E2E8F0',
},
dateText: {
fontSize: 11,
color: '#64748B',
},
message: {
marginTop: 12,
color: '#475569',
},
emptyText: {
textAlign: 'center',
color: '#64748B',
padding: 20,
lineHeight: 21,
},
errorContainer: {
padding: 18,
backgroundColor: '#FEE2E2',
borderRadius: 10,
},
errorText: {
color: '#991B1B',
marginBottom: 12,
},
retryButton: {
backgroundColor: '#2563EB',
padding: 10,
borderRadius: 8,
alignSelf: 'flex-start',
},
retryButtonText: {
color: '#FFFFFF',
fontWeight: 'bold',
},
createButton: {
  backgroundColor: '#2563EB',
  paddingVertical: 12,
  paddingHorizontal: 16,
  borderRadius: 10,
  alignItems: 'center',
  marginTop: 14,
  marginBottom: 14,
},
createButtonText: {
  color: '#FFFFFF',
  fontSize: 15,
  fontWeight: '700',
},
});

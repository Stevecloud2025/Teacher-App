import React, { useEffect, useState } from 'react';
import * as SecureStore from 'expo-secure-store';
import {
  getTeacherDashboard,
  type TeacherDashboardResponse,
} from '../api';

import { SafeAreaView } from 'react-native-safe-area-context';
import {
  Alert,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

type TeacherDashboardProps = {
fullName: string;
onLogout: () => void;
};

const quickActions = [
{ icon: '📚', title: 'My Lessons', subtitle: 'Create and manage lessons' },
{ icon: '📝', title: 'Quizzes', subtitle: 'Prepare student assessments' },
{ icon: '📋', title: 'Homework', subtitle: 'Assign and review homework' },
{ icon: '📅', title: 'Attendance', subtitle: 'Record class attendance' },
{ icon: '🎓', title: 'Grading', subtitle: 'Assess student submissions' },
{ icon: '📊', title: 'Reports', subtitle: 'Track student progress' },
];

export default function TeacherDashboard({
fullName,
onLogout,
}: TeacherDashboardProps) {
const firstName = fullName.trim().split(/\s+/)[0] || 'Teacher';

  const [dashboard, setDashboard] =
    useState<TeacherDashboardResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [dashboardError, setDashboardError] = useState<string | null>(null);

    useEffect(() => {
    let isActive = true;

    async function loadDashboard() {
      try {
        setLoading(true);
        setDashboardError(null);

        const accessToken = await SecureStore.getItemAsync(
          'teacher_app_access_token',
        );

        if (!accessToken) {
          throw new Error('Your session has expired. Please log in again.');
        }

        const result = await getTeacherDashboard(accessToken);

        if (isActive) {
          setDashboard(result);
        }
      } catch (error) {
        if (isActive) {
          setDashboardError(
            error instanceof Error
              ? error.message
              : 'Unable to load dashboard data.',
          );
        }
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      isActive = false;
    };
  }, []);

return (
  <SafeAreaView style={styles.safeArea}>
    <StatusBar barStyle="light-content" backgroundColor="#102A43" />

    <ScrollView
      contentContainerStyle={styles.scrollContent}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.brand}>TEACHER APP</Text>
            <Text style={styles.headerSubtitle}>Teacher Workspace</Text>
          </View>

          <TouchableOpacity
            style={styles.logoutButton}
            onPress={onLogout}
            accessibilityRole="button"
          >
            <Text style={styles.logoutText}>Logout</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.greeting}>Hello, {firstName} 👋</Text>

        <Text style={styles.headerMessage}>
          Ready to inspire your students today?
        </Text>

        <View style={styles.profileBadge}>
          <Text style={styles.profileBadgeText}>TEACHER ACCOUNT</Text>
        </View>
      </View>

      <View style={styles.body}>
        <Text style={styles.sectionTitle}>Your Overview</Text>

        <Text style={styles.sectionSubtitle}>
          Your teaching workspace at a glance.
        </Text>

        <View style={styles.statsGrid}>
  {[
    {
      icon: '📚',
      number: dashboard ? String(dashboard.total_lessons) : '—',
      label: 'My Lessons',
    },
    {
      icon: '📖',
      number: dashboard ? String(dashboard.published_lessons) : '—',
      label: 'Published Lessons',
    },
    {
      icon: '📝',
      number: dashboard ? String(dashboard.draft_lessons) : '—',
      label: 'Draft Lessons',
    },
    {
      icon: '🎓',
      number: dashboard ? String(dashboard.total_subjects) : '—',
      label: 'My Subjects',
    },
  ].map((item) => (
    <View key={item.label} style={styles.statCard}>
      <View style={styles.statIcon}>
        <Text>{item.icon}</Text>
      </View>

      <Text style={styles.statNumber}>{item.number}</Text>
      <Text style={styles.statLabel}>{item.label}</Text>

      <Text style={styles.sampleLabel}>
        {loading
          ? 'Loading...'
          : dashboardError
            ? 'Unavailable'
            : 'Live data'}
      </Text>
    </View>
  ))}
</View>

        {loading && (
  <Text style={styles.sectionSubtitle}>
    Loading your latest dashboard data...
  </Text>
)}

{dashboardError && (
  <View style={styles.emptyCard}>
    <Text style={styles.emptyTitle}>
      Unable to load dashboard
    </Text>

    <Text style={styles.emptyMessage}>
      {dashboardError}
    </Text>
  </View>
)}

        <View style={styles.recentSection}>
          <View style={styles.sectionHeadingRow}>
            <Text style={styles.sectionTitle}>Quick Actions</Text>
            <Text style={styles.actionCount}>6 ACTIONS</Text>
          </View>

          <View style={styles.actionsGrid}>
            {quickActions.map((action) => (
              <TouchableOpacity
                key={action.title}
                style={styles.actionCard}
                activeOpacity={0.8}
                accessibilityRole="button"
                onPress={() =>
                 Alert.alert(
                    action.title,
                    'This feature will be connected in a future step.',
                  )
                }
              >
                <View style={styles.actionIcon}>
                  <Text style={styles.actionEmoji}>{action.icon}</Text>
                </View>

                <Text style={styles.actionTitle}>{action.title}</Text>

                <Text style={styles.actionSubtitle}>
                  {action.subtitle}
                </Text>

                <Text style={styles.actionArrow}>Open →</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        ```tsx
<View style={styles.recentSection}>
  <View style={styles.sectionHeadingRow}>
    <Text style={styles.sectionTitle}>Recent Lessons</Text>
    <Text style={styles.actionCount}>
      {dashboard ? `${dashboard.recent_lessons_count} LESSONS` : '—'}
    </Text>
  </View>

  {loading ? (
    <View style={styles.emptyCard}>
      <Text style={styles.emptyMessage}>
        Loading your recent lessons...
      </Text>
    </View>
  ) : dashboardError ? (
    <View style={styles.emptyCard}>
      <Text style={styles.emptyIcon}>⚠️</Text>
      <Text style={styles.emptyTitle}>Lessons unavailable</Text>
      <Text style={styles.emptyMessage}>
        Your recent lessons could not be loaded.
      </Text>
    </View>
  ) : dashboard && dashboard.recent_lessons.length > 0 ? (
    dashboard.recent_lessons.map((lesson) => (
      <View key={lesson.id} style={styles.lessonCard}>
        <View style={styles.lessonCardTop}>
          <Text style={styles.lessonTitle}>{lesson.title}</Text>

          <View style={styles.lessonStatusBadge}>
            <Text style={styles.lessonStatusText}>
              {lesson.status}
            </Text>
          </View>
        </View>

        <Text style={styles.lessonDetails}>
          {lesson.subject} • {lesson.class_name}
        </Text>

        <Text style={styles.lessonTopic}>
          Topic: {lesson.topic}
        </Text>
      </View>
    ))
  ) : (
    <View style={styles.emptyCard}>
      <Text style={styles.emptyIcon}>📚</Text>
      <Text style={styles.emptyTitle}>No lessons yet</Text>
      <Text style={styles.emptyMessage}>
        Lessons you create will appear here.
      </Text>
    </View>
  )}
</View>
```


        <View style={styles.footer}>
          <Text style={styles.footerBrand}>TEACHER APP</Text>
          <Text style={styles.footerText}>Teach. Inspire. Empower.</Text>
        </View>
      </View>
    </ScrollView>
  </SafeAreaView>
);

}

const styles = StyleSheet.create({
safeArea: {
flex: 1,
backgroundColor: '#F4F7FB',
},
scrollContent: {
flexGrow: 1,
},
header: {
backgroundColor: '#102A43',
paddingHorizontal: 22,
paddingTop: 18,
paddingBottom: 34,
borderBottomLeftRadius: 28,
borderBottomRightRadius: 28,
},
headerTop: {
flexDirection: 'row',
justifyContent: 'space-between',
alignItems: 'center',
},
brand: {
color: '#FFFFFF',
fontSize: 13,
fontWeight: '800',
letterSpacing: 2,
},
headerSubtitle: {
color: '#B7C9D9',
fontSize: 12,
marginTop: 5,
},
logoutButton: {
paddingHorizontal: 15,
paddingVertical: 9,
borderRadius: 10,
borderWidth: 1,
borderColor: '#54738E',
},
logoutText: {
color: '#FFFFFF',
fontWeight: '600',
fontSize: 12,
},
greeting: {
color: '#FFFFFF',
fontSize: 28,
fontWeight: '800',
marginTop: 34,
},
headerMessage: {
color: '#D5E2ED',
fontSize: 14,
lineHeight: 21,
marginTop: 8,
},
profileBadge: {
alignSelf: 'flex-start',
backgroundColor: '#1C4962',
paddingHorizontal: 12,
paddingVertical: 7,
borderRadius: 20,
marginTop: 18,
},
profileBadgeText: {
color: '#8DE0CA',
fontSize: 10,
fontWeight: '800',
letterSpacing: 1,
},
body: {
paddingHorizontal: 20,
paddingTop: 26,
paddingBottom: 24,
},
sectionTitle: {
color: '#102A43',
fontSize: 19,
fontWeight: '800',
},
sectionSubtitle: {
color: '#718096',
fontSize: 13,
marginTop: 5,
marginBottom: 18,
},
statsGrid: {
flexDirection: 'row',
flexWrap: 'wrap',
justifyContent: 'space-between',
gap: 12,
},
statCard: {
width: '48%',
backgroundColor: '#FFFFFF',
borderRadius: 17,
padding: 15,
borderWidth: 1,
borderColor: '#E7EDF4',
minHeight: 148,
},
statIcon: {
width: 38,
height: 38,
borderRadius: 12,
alignItems: 'center',
justifyContent: 'center',
},
statNumber: {
color: '#102A43',
fontSize: 25,
fontWeight: '800',
marginTop: 12,
},
statLabel: {
color: '#526579',
fontSize: 12,
fontWeight: '600',
marginTop: 3,
},
sampleLabel: {
color: '#9AA8B7',
fontSize: 10,
marginTop: 5,
},
sectionHeadingRow: {
flexDirection: 'row',
alignItems: 'center',
justifyContent: 'space-between',
marginBottom: 15,
},
actionCount: {
color: '#0D9B83',
fontSize: 10,
fontWeight: '800',
letterSpacing: 1,
},
actionsGrid: {
flexDirection: 'row',
flexWrap: 'wrap',
justifyContent: 'space-between',
gap: 12,
},
actionCard: {
width: '48%',
backgroundColor: '#FFFFFF',
borderWidth: 1,
borderColor: '#E7EDF4',
borderRadius: 17,
padding: 14,
minHeight: 168,
},
actionIcon: {
width: 42,
height: 42,
borderRadius: 13,
backgroundColor: '#E6F6F2',
alignItems: 'center',
justifyContent: 'center',
},
actionEmoji: {
fontSize: 21,
},
actionTitle: {
color: '#102A43',
fontSize: 14,
fontWeight: '800',
marginTop: 13,
},
actionSubtitle: {
color: '#718096',
fontSize: 11,
lineHeight: 16,
marginTop: 5,
},
actionArrow: {
color: '#0D9B83',
fontSize: 11,
fontWeight: '700',
marginTop: 'auto',
paddingTop: 12,
},
recentSection: {
marginTop: 30,
},
recentBadge: {
color: '#718096',
fontSize: 10,
fontWeight: '800',
letterSpacing: 1,
},
emptyCard: {
alignItems: 'center',
backgroundColor: '#FFFFFF',
borderWidth: 1,
borderColor: '#E7EDF4',
borderRadius: 18,
paddingHorizontal: 24,
paddingVertical: 28,
},
emptyIcon: {
fontSize: 34,
},
emptyTitle: {
color: '#102A43',
fontSize: 14,
fontWeight: '800',
textAlign: 'center',
marginTop: 12,
},
emptyMessage: {
color: '#718096',
fontSize: 12,
lineHeight: 18,
textAlign: 'center',
marginTop: 7,
},
footer: {
alignItems: 'center',
paddingTop: 30,
paddingBottom: 10,
},
footerBrand: {
color: '#102A43',
fontSize: 11,
fontWeight: '800',
letterSpacing: 2,
},
footerText: {
  color: '#8A98A8',
  fontSize: 11,
  marginTop: 6,
},

lessonCard: {
  backgroundColor: '#FFFFFF',
  borderWidth: 1,
  borderColor: '#E7EDF4',
  borderRadius: 16,
  padding: 15,
  marginBottom: 12,
},

lessonCardTop: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'flex-start',
  gap: 10,
},

lessonTitle: {
  flex: 1,
  color: '#102A43',
  fontSize: 14,
  fontWeight: '800',
},

lessonStatusBadge: {
  backgroundColor: '#E6F6F2',
  paddingHorizontal: 9,
  paddingVertical: 5,
  borderRadius: 12,
},

lessonStatusText: {
  color: '#0D806F',
  fontSize: 10,
  fontWeight: '800',
  textTransform: 'capitalize',
},

lessonDetails: {
  color: '#526579',
  fontSize: 12,
  marginTop: 10,
},

lessonTopic: {
  color: '#718096',
  fontSize: 12,
  marginTop: 6,
},
});
import React from 'react';
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

type StudentDashboardProps = {
fullName: string;
onLogout: () => void;
};

const learningActions = [
{
icon: '📚',
title: 'My Lessons',
subtitle: 'Explore your learning materials',
},
{
icon: '📝',
title: 'Take Quizzes',
subtitle: 'Test your knowledge',
},
{
icon: '📋',
title: 'Homework',
subtitle: 'View and submit assignments',
},
{
icon: '📊',
title: 'My Results',
subtitle: 'Review your scores and grades',
},
];

export default function StudentDashboard({
fullName,
onLogout,
}: StudentDashboardProps) {
const firstName = fullName.trim().split(/\s+/)[0] || 'Student';

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
            <Text style={styles.headerSubtitle}>
              Student Learning Space
            </Text>
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
          Keep learning, keep growing, and do your best today.
        </Text>

        <View style={styles.profileBadge}>
          <Text style={styles.profileBadgeText}>STUDENT ACCOUNT</Text>
        </View>
      </View>

      <View style={styles.body}>
        <Text style={styles.sectionTitle}>My Learning</Text>

        <Text style={styles.sectionSubtitle}>
          Here is an overview of your learning activities.
        </Text>

        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <View
              style={[styles.statIcon, { backgroundColor: '#DDF5EE' }]}
            >
              <Text>📚</Text>
            </View>
            <Text style={styles.statNumber}>0</Text>
            <Text style={styles.statLabel}>Available Lessons</Text>
            <Text style={styles.sampleLabel}>Sample data</Text>
          </View>

          <View style={styles.statCard}>
            <View
              style={[styles.statIcon, { backgroundColor: '#E5EDFF' }]}
            >
              <Text>📝</Text>
            </View>
            <Text style={styles.statNumber}>0</Text>
            <Text style={styles.statLabel}>Pending Quizzes</Text>
            <Text style={styles.sampleLabel}>Sample data</Text>
          </View>

          <View style={styles.statCard}>
            <View
              style={[styles.statIcon, { backgroundColor: '#FFF0D9' }]}
            >
              <Text>📋</Text>
            </View>
            <Text style={styles.statNumber}>0</Text>
            <Text style={styles.statLabel}>Pending Homework</Text>
            <Text style={styles.sampleLabel}>Sample data</Text>
          </View>

          <View style={styles.statCard}>
            <View
              style={[styles.statIcon, { backgroundColor: '#F0E5FF' }]}
            >
              <Text>🎯</Text>
            </View>
            <Text style={styles.statNumber}>—</Text>
            <Text style={styles.statLabel}>Quiz Average</Text>
            <Text style={styles.sampleLabel}>Not connected yet</Text>
          </View>
        </View>

        <View style={styles.sectionHeadingRow}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <Text style={styles.actionCount}>4 FEATURES</Text>
        </View>

        <View style={styles.actionsGrid}>
          {learningActions.map((action) => (
            <TouchableOpacity
              key={action.title}
              activeOpacity={0.8}
              style={styles.actionCard}
              onPress={() =>
                Alert.alert(
                  action.title,
                  'This feature will be connected in a future step.',
                )
              }
              accessibilityRole="button"
              accessibilityLabel={action.title}
            >
              <View style={styles.actionIcon}>
                <Text style={styles.actionEmoji}>{action.icon}</Text>
              </View>

              <Text style={styles.actionTitle}>{action.title}</Text>

              <Text style={styles.actionSubtitle}>
                {action.subtitle}
              </Text>

              <Text style={styles.actionArrow}>Explore →</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.progressSection}>
          <Text style={styles.sectionTitle}>Learning Progress</Text>

          <View style={styles.progressCard}>
            <View style={styles.progressIcon}>
              <Text style={styles.progressEmoji}>🌱</Text>
            </View>

            <Text style={styles.progressTitle}>
              Your progress starts here
            </Text>

            <Text style={styles.progressMessage}>
              Complete lessons, take quizzes, and submit homework to build
              your learning record.
            </Text>

            <View style={styles.progressTrack}>
              <View style={styles.progressFill} />
            </View>

            <Text style={styles.progressCaption}>
              Progress statistics will appear when connected to your account.
            </Text>
          </View>
        </View>

        <View style={styles.recentSection}>
          <View style={styles.sectionHeadingRow}>
            <Text style={styles.sectionTitle}>Recent Activity</Text>
            <Text style={styles.recentBadge}>LATEST</Text>
          </View>

          <View style={styles.emptyCard}>
            <Text style={styles.emptyIcon}>📖</Text>

            <Text style={styles.emptyTitle}>
              Your learning journey awaits
            </Text>

            <Text style={styles.emptyMessage}>
              Your recent lessons, quiz attempts, and homework submissions
              will appear here.
            </Text>
          </View>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerBrand}>TEACHER APP</Text>

          <Text style={styles.footerText}>
            Learn with purpose. Grow with confidence.
          </Text>
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
marginTop: 12,
},
progressSection: {
marginTop: 30,
},
progressCard: {
backgroundColor: '#FFFFFF',
borderWidth: 1,
borderColor: '#E7EDF4',
borderRadius: 18,
padding: 20,
marginTop: 15,
},
progressIcon: {
width: 46,
height: 46,
borderRadius: 14,
backgroundColor: '#DDF5EE',
alignItems: 'center',
justifyContent: 'center',
},
progressEmoji: {
fontSize: 23,
},
progressTitle: {
color: '#102A43',
fontSize: 15,
fontWeight: '800',
marginTop: 14,
},
progressMessage: {
color: '#718096',
fontSize: 12,
lineHeight: 19,
marginTop: 7,
},
progressTrack: {
height: 7,
backgroundColor: '#E8EEF4',
borderRadius: 10,
marginTop: 18,
overflow: 'hidden',
},
progressFill: {
width: '0%',
height: '100%',
backgroundColor: '#0D9B83',
borderRadius: 10,
},
progressCaption: {
color: '#9AA8B7',
fontSize: 10,
lineHeight: 15,
marginTop: 9,
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
});

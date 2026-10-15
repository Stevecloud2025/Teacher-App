
import { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import * as SecureStore from 'expo-secure-store';
import { loginUser } from './src/api';
import TeacherDashboard from './src/screens/TeacherDashboard';
import StudentDashboard from './src/screens/StudentDashboard';
import {
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

type UserRole = 'teacher' | 'student';

export default function App() {
  const [role, setRole] = useState<UserRole>('teacher');
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [showPassword, setShowPassword] = useState(false);
const [isLoading, setIsLoading] = useState(false);
const [signedInUser, setSignedInUser] = useState<{
  role: UserRole;
  full_name: string;
  userId: number | undefined;
} | null>(null);

  const handleLogin = async () => {
  if (!email.trim() || !password) {
    Alert.alert(
      'Missing information',
      'Please enter your email address and password.',
    );
    return;
  }

  if (isLoading) {
    return;
  }

  setIsLoading(true);

  try {
    const result = await loginUser(role, email, password);

    // Save the access token securely on the phone.
    await SecureStore.setItemAsync(
      'teacher_app_access_token',
      result.access_token,
    );

    // Save the signed-in user's basic information.
    const userId =
      role === 'teacher' ? result.teacher_id : result.student_id;

    await SecureStore.setItemAsync(
      'teacher_app_user',
      JSON.stringify({
        role,
        userId,
        full_name: result.full_name,
        email: result.email,
      }),
    );

    setSignedInUser({
  role,
  full_name: result.full_name,
  userId,
});

setPassword('');

  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : 'Unable to connect to the server. Please try again.';

    Alert.alert('Login failed', message);
  } finally {
    setIsLoading(false);
  }
};

const handleLogout = async () => {
  try {
    await SecureStore.deleteItemAsync('teacher_app_access_token');
    await SecureStore.deleteItemAsync('teacher_app_user');
  } catch (error) {
    Alert.alert(
      'Logout notice',
      'Your session could not be fully cleared. Please try again.',
    );
    return;
  }

  setSignedInUser(null);
  setEmail('');
  setPassword('');
  setShowPassword(false);
  setRole('teacher');
};

if (signedInUser?.role === 'teacher') {
  return (
    <TeacherDashboard
      fullName={signedInUser.full_name}
      onLogout={handleLogout}
    />
  );
}

if (signedInUser?.role === 'student') {
  return (
    <StudentDashboard
      fullName={signedInUser.full_name}
      onLogout={handleLogout}
    />
  );
}
  return (
    <View style={styles.screen}>
      <StatusBar style="light" />

      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Brand header */}
          <View style={styles.header}>
            <View style={styles.decorativeCircle} />
            <View style={styles.decorativeCircleSmall} />

            {/* Custom Teacher App logo */}
            <View
              style={styles.logo}
              accessible
              accessibilityLabel="Teacher App logo, representing teaching and learning"
            >
              {/* Graduation cap */}
              <View style={styles.cap}>
                <View style={styles.capTop} />
                <View style={styles.capBase} />
                <View style={styles.capTassel} />
              </View>

              {/* Open book */}
              <View style={styles.logoBook}>
                <View style={styles.logoPageLeft}>
                  <Text style={styles.logoLetter}>T</Text>
                </View>

                <View style={styles.logoPageRight}>
                  <Text style={styles.logoLetter}>A</Text>
                </View>
              </View>
            </View>

            <Text style={styles.brandName}>Teacher App</Text>

            <Text style={styles.brandSubtitle}>
              SCHOOLS MANAGEMENT APP
            </Text>

            <View style={styles.headerMessage}>
              <Text style={styles.welcomeText}>
                Welcome to your{'\n'}learning space.
              </Text>

              <Text style={styles.headerDescription}>
                Teaching, learning and progress —{'\n'}
                all in one place.
              </Text>
            </View>
          </View>

          {/* Login form */}
          <View style={styles.formContainer}>
            <Text style={styles.formTitle}>Sign in</Text>

            <Text style={styles.formSubtitle}>
              Select your account type to continue.
            </Text>

            {/* Account type selector */}
            <View style={styles.roleSelector}>
              <TouchableOpacity
                activeOpacity={0.8}
                accessibilityRole="button"
                accessibilityState={{ selected: role === 'teacher' }}
                style={[
                  styles.roleButton,
                  role === 'teacher' && styles.roleButtonActive,
                ]}
                onPress={() => setRole('teacher')}
              >
                <Text style={styles.roleIcon}>▤</Text>

                <Text
                  style={[
                    styles.roleText,
                    role === 'teacher' && styles.roleTextActive,
                  ]}
                >
                  Teacher
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                activeOpacity={0.8}
                accessibilityRole="button"
                accessibilityState={{ selected: role === 'student' }}
                style={[
                  styles.roleButton,
                  role === 'student' && styles.roleButtonActive,
                ]}
                onPress={() => setRole('student')}
              >
                <Text style={styles.roleIcon}>♙</Text>

                <Text
                  style={[
                    styles.roleText,
                    role === 'student' && styles.roleTextActive,
                  ]}
                >
                  Student
                </Text>
              </TouchableOpacity>
            </View>

            {/* Email field */}
            <Text style={styles.label}>Email address</Text>

            <View style={styles.inputContainer}>
              <Text style={styles.inputIcon}>✉</Text>

              <TextInput
                style={styles.input}
                placeholder="Enter your email"
                placeholderTextColor="#98A2B3"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                autoComplete="email"
                accessibilityLabel="Email address"
              />
            </View>

            {/* Password field */}
            <Text style={styles.label}>Password</Text>

            <View style={styles.inputContainer}>
              <Text style={styles.inputIcon}>●</Text>

              <TextInput
                style={styles.input}
                placeholder="Enter your password"
                placeholderTextColor="#98A2B3"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                autoComplete="current-password"
                accessibilityLabel="Password"
              />

              <TouchableOpacity
                onPress={() => setShowPassword(!showPassword)}
                accessibilityRole="button"
                accessibilityLabel={
                  showPassword ? 'Hide password' : 'Show password'
                }
              >
                <Text style={styles.showPassword}>
                  {showPassword ? 'Hide' : 'Show'}
                </Text>
              </TouchableOpacity>
            </View>

            {/* Forgot password */}
            <TouchableOpacity
              style={styles.forgotPassword}
              accessibilityRole="button"
              onPress={() =>
                Alert.alert(
                  'Password recovery',
                  'Password recovery will be added in a future step.',
                )
              }
            >
              <Text style={styles.forgotPasswordText}>
                Forgot password?
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
  activeOpacity={0.85}
  style={[
    styles.loginButton,
    isLoading && { opacity: 0.7 },
  ]}
  accessibilityRole="button"
  accessibilityState={{ disabled: isLoading }}
  disabled={isLoading}
  onPress={handleLogin}
>
  <Text style={styles.loginButtonText}>
    {isLoading ? 'Signing in...' : 'Sign In'}
  </Text>

  {!isLoading && (
    <Text style={styles.loginArrow}>→</Text>
  )}
</TouchableOpacity>

            {/* Security message */}
            <View style={styles.securityNote}>
              <Text style={styles.securityIcon}>✓</Text>

              <Text style={styles.securityText}>
                Your learning community, securely connected.
              </Text>
            </View>
          </View>

          {/* Footer */}
          <Text style={styles.footer}>
            TEACHER APP FOR SCHOOLS {'  •  '} LEARN. GROW. EXCEL.
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#F4F7FB',
  },

  keyboardView: {
    flex: 1,
  },

  scrollContent: {
    flexGrow: 1,
    paddingBottom: 22,
  },

  header: {
    backgroundColor: '#142744',
    paddingTop: Platform.OS === 'android' ? 46 : 62,
    paddingHorizontal: 28,
    paddingBottom: 72,
    borderBottomLeftRadius: 36,
    borderBottomRightRadius: 36,
    overflow: 'hidden',
  },

  decorativeCircle: {
    position: 'absolute',
    width: 220,
    height: 220,
    borderRadius: 110,
    backgroundColor: 'rgba(45, 203, 179, 0.09)',
    right: -75,
    top: -65,
  },

  decorativeCircleSmall: {
    position: 'absolute',
    width: 135,
    height: 135,
    borderRadius: 68,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    right: 18,
    top: 48,
  },

  /* Main logo container */
  logo: {
    width: 58,
    height: 58,
    borderRadius: 17,
    backgroundColor: '#2DCBB3',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
    position: 'relative',
    overflow: 'hidden',
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 4,
  },

  /* Graduation cap */
  cap: {
    position: 'absolute',
    top: 5,
    width: 27,
    height: 17,
    alignItems: 'center',
    zIndex: 2,
  },

  capTop: {
    width: 22,
    height: 9,
    backgroundColor: '#142744',
    transform: [{ rotate: '45deg' }],
    borderRadius: 2,
    position: 'absolute',
    top: 0,
  },

  capBase: {
    width: 22,
    height: 5,
    backgroundColor: '#FFFFFF',
    borderRadius: 3,
    position: 'absolute',
    top: 8,
  },

  capTassel: {
    width: 3,
    height: 8,
    backgroundColor: '#142744',
    position: 'absolute',
    right: 2,
    top: 7,
    borderRadius: 2,
  },

  /* Open book */
  logoBook: {
    position: 'absolute',
    bottom: 7,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },

  logoPageLeft: {
    width: 22,
    height: 24,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#142744',
    borderTopLeftRadius: 5,
    borderBottomLeftRadius: 3,
    alignItems: 'center',
    justifyContent: 'center',
  },

  logoPageRight: {
    width: 22,
    height: 24,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#142744',
    borderTopRightRadius: 5,
    borderBottomRightRadius: 3,
    alignItems: 'center',
    justifyContent: 'center',
  },

  logoLetter: {
    color: '#142744',
    fontSize: 14,
    fontWeight: '900',
  },

  brandName: {
    color: '#FFFFFF',
    fontSize: 23,
    fontWeight: '800',
    letterSpacing: 0.3,
  },

  brandSubtitle: {
    color: '#A9B8CC',
    fontSize: 9,
    fontWeight: '700',
    letterSpacing: 2.2,
    marginTop: 4,
  },

  headerMessage: {
    marginTop: 35,
  },

  welcomeText: {
    color: '#FFFFFF',
    fontSize: 31,
    fontWeight: '800',
    lineHeight: 39,
    letterSpacing: -0.5,
  },

  headerDescription: {
    color: '#CAD5E4',
    fontSize: 14,
    lineHeight: 22,
    marginTop: 11,
  },

  /* Login card */
  formContainer: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    marginTop: -36,
    paddingHorizontal: 22,
    paddingTop: 26,
    paddingBottom: 24,
    borderRadius: 24,
    shadowColor: '#142744',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.08,
    shadowRadius: 18,
    elevation: 5,
  },

  formTitle: {
    color: '#142744',
    fontSize: 25,
    fontWeight: '800',
  },

  formSubtitle: {
    color: '#778399',
    fontSize: 13,
    marginTop: 7,
    marginBottom: 22,
  },

  /* Teacher/student selector */
  roleSelector: {
    flexDirection: 'row',
    backgroundColor: '#F1F4F8',
    padding: 5,
    borderRadius: 14,
    marginBottom: 25,
  },

  roleButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 13,
    borderRadius: 10,
    gap: 8,
  },

  roleButtonActive: {
    backgroundColor: '#FFFFFF',
    shadowColor: '#142744',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 5,
    elevation: 2,
  },

  roleIcon: {
    fontSize: 18,
    color: '#52627A',
  },

  roleText: {
    color: '#778399',
    fontSize: 13,
    fontWeight: '600',
  },

  roleTextActive: {
    color: '#142744',
    fontWeight: '800',
  },

  /* Input fields */
  label: {
    color: '#273750',
    fontSize: 13,
    fontWeight: '700',
    marginBottom: 9,
  },

  inputContainer: {
    minHeight: 54,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: '#E4E9F0',
    borderRadius: 13,
    paddingHorizontal: 14,
    marginBottom: 19,
  },

  inputIcon: {
    color: '#7C8BA1',
    fontSize: 17,
    marginRight: 11,
  },

  input: {
    flex: 1,
    color: '#142744',
    fontSize: 14,
    paddingVertical: 13,
  },

  showPassword: {
    color: '#188F82',
    fontSize: 12,
    fontWeight: '700',
    paddingLeft: 8,
  },

  /* Password recovery */
  forgotPassword: {
    alignSelf: 'flex-end',
    marginTop: -5,
    marginBottom: 22,
  },

  forgotPasswordText: {
    color: '#188F82',
    fontSize: 12,
    fontWeight: '700',
  },

  /* Sign-in button */
  loginButton: {
    minHeight: 55,
    backgroundColor: '#142744',
    borderRadius: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },

  loginButtonText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '800',
    letterSpacing: 0.4,
  },

  loginArrow: {
    position: 'absolute',
    right: 20,
    color: '#2DCBB3',
    fontSize: 23,
    fontWeight: '600',
  },

  /* Security message */
  securityNote: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 21,
    gap: 7,
  },

  securityIcon: {
    width: 17,
    height: 17,
    borderRadius: 9,
    overflow: 'hidden',
    textAlign: 'center',
    textAlignVertical: 'center',
    backgroundColor: '#DDF7F1',
    color: '#138675',
    fontSize: 11,
    fontWeight: '900',
  },

  securityText: {
    color: '#8994A5',
    fontSize: 10,
  },

  /* Footer */
  footer: {
    textAlign: 'center',
    color: '#9AA5B5',
    fontSize: 9,
    fontWeight: '700',
    letterSpacing: 1,
    marginTop: 25,
    marginHorizontal: 12,
  },
});
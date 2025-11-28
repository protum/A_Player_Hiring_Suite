// Core Types for A-Player Hiring Suite

export interface Candidate {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  current_title?: string;
  linkedin_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Outcome {
  id?: string;
  description: string;
  metric?: string;
  timeframe?: string;
  priority?: number;
}

export interface Indicator {
  id?: string;
  indicator: string;
}

export interface Competency {
  id?: string;
  name: string;
  definition?: string;
  indicators: Indicator[];
}

export interface Scorecard {
  id: string;
  role_title: string;
  mission: string;
  department?: string;
  created_by?: string;
  created_at: string;
  updated_at: string;
  outcomes: Outcome[];
  competencies: Competency[];
}

export interface JobHistory {
  id?: string;
  company: string;
  title: string;
  start_date?: string;
  end_date?: string;
  sequence_order?: number;
  responsibilities?: string;
  questions: InterviewQuestion[];
}

export interface InterviewQuestion {
  id?: string;
  question_type: string;
  question_text: string;
  response?: string;
  rating?: number;
  notes?: string;
}

export interface RedFlag {
  id?: string;
  flag_type: string;
  description: string;
  severity?: string;
  job_history_id?: string;
  created_at?: string;
}

export interface Interview {
  id: string;
  candidate_id: string;
  scorecard_id?: string;
  interview_date?: string;
  interviewer_name?: string;
  status: string;
  overall_rating?: string;
  hire_recommendation?: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
  job_history: JobHistory[];
  red_flags: RedFlag[];
}

export interface BehaviorRating {
  id?: string;
  behavior: 'decisiveness' | 'reliability' | 'adaptation' | 'engagement';
  score: number;
  evidence?: string;
  development_notes?: string;
}

export interface CEOAssessment {
  id: string;
  subject_id: string;
  assessment_date: string;
  assessment_type: 'self' | 'observer' | '360';
  assessor_name?: string;
  overall_score?: number;
  notes?: string;
  created_at: string;
  behavior_ratings: BehaviorRating[];
}

export interface PowerScoreResponse {
  id?: string;
  dimension: 'results' | 'relationships' | 'role_model';
  question_id: string;
  question_text: string;
  response_value?: number;
  response_text?: string;
}

export interface DevelopmentPlan {
  id?: string;
  dimension: 'results' | 'relationships' | 'role_model';
  goal: string;
  action_steps?: string;
  target_date?: string;
  status?: string;
}

export interface PowerScoreAssessment {
  id: string;
  subject_id: string;
  assessment_date: string;
  results_score: number;
  relationships_score: number;
  role_model_score: number;
  overall_power_score: number;
  notes?: string;
  created_at: string;
  responses: PowerScoreResponse[];
  development_plans: DevelopmentPlan[];
}

// Ideal Team Player Types
export interface VirtueRating {
  id?: string;
  virtue: 'humble' | 'hungry' | 'smart';
  question_id: string;
  question_text: string;
  response_value: number;
  evidence?: string;
}

export interface IdealTeamPlayerAssessment {
  id: string;
  subject_id: string;
  assessment_date: string;
  assessment_type: 'self' | 'observer' | 'interview';
  assessor_name?: string;
  humble_score: number;
  hungry_score: number;
  smart_score: number;
  overall_score: number;
  category?: string;
  notes?: string;
  created_at: string;
  virtue_ratings: VirtueRating[];
}

// Core Values Types
export interface CoreValueRating {
  id?: string;
  value: 'personal_growth' | 'harmonious_relationships' | 'problem_solving' | 'positive_impact' | 'financial_stewardship';
  question_id: string;
  question_text: string;
  response_value: number;
  evidence?: string;
}

export interface CoreValuesAssessment {
  id: string;
  subject_id: string;
  assessment_date: string;
  assessment_type: 'interview' | 'behavioral' | 'reference';
  assessor_name?: string;
  personal_growth_score: number;
  harmonious_relationships_score: number;
  problem_solving_score: number;
  positive_impact_score: number;
  financial_stewardship_score: number;
  overall_alignment_score: number;
  alignment_level?: string;
  notes?: string;
  created_at: string;
  value_ratings: CoreValueRating[];
}

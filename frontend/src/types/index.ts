/**
 * TypeScript type definitions for A-Player Hiring Suite
 */

export type UserRole =
  | 'admin'
  | 'board_member'
  | 'founder'
  | 'ceo'
  | 'executive_coach'
  | 'hr_manager';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  organization_id?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Scorecard {
  id: string;
  organization_id: string;
  created_by_id?: string;
  role_title: string;
  role_mission: string;
  status: 'draft' | 'active' | 'archived';
  created_at: string;
  updated_at: string;
  outcomes?: ScorecardOutcome[];
  competencies?: ScorecardCompetency[];
}

export interface ScorecardOutcome {
  id: string;
  scorecard_id: string;
  description: string;
  metric: string;
  target_value: string;
  timeframe: string;
  priority: number;
}

export interface ScorecardCompetency {
  id: string;
  scorecard_id: string;
  competency_name: string;
  description: string;
  behavioral_anchors: Record<string, any>;
  weight: number;
}

export interface CEOScorecard {
  id: string;
  ceo_id: string;
  organization_id: string;
  period: string;
  ceo_excellence_index?: number;
  status: 'draft' | 'finalized' | 'archived';
  created_at: string;
  updated_at: string;
  finalized_at?: string;
}

export interface CEOBehaviorScore {
  id: string;
  ceo_scorecard_id: string;
  // Decisiveness
  decision_speed?: number;
  decision_quality?: number;
  loss_cutting?: number;
  ambiguity_handling?: number;
  // Reliability
  predictability?: number;
  commitment_delivery?: number;
  process_discipline?: number;
  time_management?: number;
  // Bold Adaptation
  pivot_capacity?: number;
  inflection_recognition?: number;
  experimentation_velocity?: number;
  learning_agility?: number;
  // Engaging for Impact
  stakeholder_influence?: number;
  cross_functional_alignment?: number;
  vision_communication?: number;
  talent_magnetism?: number;
  // Aggregate scores
  decisiveness_score?: number;
  reliability_score?: number;
  bold_adaptation_score?: number;
  engaging_impact_score?: number;
  overall_behavior_score?: number;
  weakest_behavior?: string;
  strongest_behavior?: string;
}

export interface CEOPowerScore {
  id: string;
  ceo_scorecard_id: string;
  // Priorities (P)
  clarity_score?: number;
  focus_score?: number;
  alignment_score?: number;
  resource_consistency_score?: number;
  // Who (W)
  bench_strength_score?: number;
  a_player_ratio_score?: number;
  team_gaps_score?: number;
  delegation_efficiency_score?: number;
  // Relationships (R)
  board_alignment_score?: number;
  cross_team_collaboration_score?: number;
  market_trust_score?: number;
  culture_health_score?: number;
  // Aggregate scores
  priorities_score?: number;
  who_score?: number;
  relationships_score?: number;
  total_power_score?: number;
  weakest_dimension?: string;
  weakest_sub_component?: string;
}

export interface CEOOperatingMetrics {
  id: string;
  ceo_scorecard_id: string;
  quarterly_goal_achievement?: number;
  revenue_target_performance?: number;
  cash_runway_discipline?: number;
  strategy_execution_score?: number;
  people_leadership_score?: number;
  org_engagement_score?: number;
  customer_impact_score?: number;
  overall_operating_score?: number;
  revenue_actual?: number;
  revenue_target?: number;
  cash_runway_months?: number;
  team_size?: number;
  customer_nps?: number;
}

export interface CEORecommendation {
  id: string;
  ceo_scorecard_id: string;
  recommendation_type: 'behavior_improvement' | 'power_score_improvement' | 'failure_point_mitigation';
  priority: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  action_items: any[];
  expected_impact?: string;
  status: string;
}

export interface Interview {
  id: string;
  candidate_name: string;
  candidate_email?: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  overall_rating?: number;
  cqi_score?: number;
  recommendation?: string;
}

export interface LeadershipAssessment {
  id: string;
  subject_id: string;
  assessment_period: string;
  status: 'pending' | 'in_progress' | 'completed';
  decisiveness_score?: number;
  reliability_score?: number;
  bold_adaptation_score?: number;
  engaging_impact_score?: number;
  overall_score?: number;
}

export interface PowerScore {
  id: string;
  executive_id: string;
  assessment_date: string;
  priorities_score?: number;
  who_score?: number;
  relationships_score?: number;
  total_power_score?: number;
  weakest_dimension?: string;
}

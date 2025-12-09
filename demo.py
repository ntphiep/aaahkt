"""
Demo script to showcase the AWS DevOps Pipeline functionality.

This script demonstrates the complete workflow without requiring actual AWS credentials.
It uses mock data to show how the system would work in production.
"""

import json
from datetime import datetime
from src.kestra.ai_agent import KestraAIAgent
from src.oumi.rl_agent import DeploymentRLAgent


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_kestra_ai_agent():
    """Demonstrate Kestra AI Agent functionality."""
    print_section("Kestra AI Agent Demo")
    
    agent = KestraAIAgent()
    
    # Mock log data
    mock_logs = [
        {'message': 'INFO: Request processed successfully'},
        {'message': 'ERROR: Connection timeout to database'},
        {'message': 'ERROR: Memory limit exceeded'},
        {'message': 'WARNING: High response time detected'},
        {'message': 'ERROR: Failed to connect to external API'},
        {'message': 'CRITICAL: Service unavailable'},
    ]
    
    print("📋 Analyzing CloudWatch logs...")
    log_summary = agent.summarize_cloudwatch_logs(mock_logs)
    
    print(json.dumps(log_summary, indent=2))
    
    # Mock metrics
    mock_metrics = {
        'invocations': 1000,
        'errors': 50,
        'error_rate': 5.0,
        'duration': 250,
        'throttles': 2
    }
    
    print("\n📊 Analyzing Lambda metrics...")
    metrics_analysis = agent.analyze_lambda_metrics(mock_metrics)
    
    print(json.dumps(metrics_analysis, indent=2))
    
    print("\n🤔 Making deployment decision...")
    decision = agent.make_deployment_decision(log_summary, metrics_analysis)
    
    print(json.dumps(decision, indent=2))
    
    return log_summary, metrics_analysis, decision


def demo_rl_agent():
    """Demonstrate Oumi RL Agent functionality."""
    print_section("Oumi RL Agent Demo")
    
    agent = DeploymentRLAgent()
    
    # Mock current metrics
    current_metrics = {
        'error_rate': 3.5,
        'cost': 85.0,
        'duration': 300
    }
    
    print("🧠 Getting RL optimization recommendation...")
    recommendation = agent.optimize_deployment_strategy(current_metrics)
    
    print(json.dumps(recommendation, indent=2))
    
    # Simulate training with feedback
    print("\n📚 Simulating RL training...")
    
    metrics_before = {'error_rate': 5.0, 'cost': 100.0}
    metrics_after = {'error_rate': 2.5, 'cost': 85.0}
    
    state = agent.get_state(metrics_before)
    action = agent.choose_action(state)
    reward = agent.calculate_reward(action, metrics_before, metrics_after)
    next_state = agent.get_state(metrics_after)
    
    print(f"State: {state}")
    print(f"Action: {action}")
    print(f"Reward: {reward:.2f}")
    print(f"Next State: {next_state}")
    
    agent.update_q_value(state, action, reward, next_state)
    
    print("\n📈 RL Training Statistics:")
    stats = agent.get_training_stats()
    print(json.dumps(stats, indent=2))
    
    return recommendation


def demo_combined_decision():
    """Demonstrate combined decision-making."""
    print_section("Combined Decision Making Demo")
    
    kestra_agent = KestraAIAgent()
    rl_agent = DeploymentRLAgent()
    
    # Scenario 1: Healthy system
    print("Scenario 1: Healthy System")
    print("-" * 40)
    
    healthy_logs = [
        {'message': 'INFO: Request processed'},
        {'message': 'INFO: Cache hit'},
    ]
    
    healthy_metrics = {
        'invocations': 1000,
        'errors': 2,
        'error_rate': 0.2,
        'duration': 150,
        'cost': 50.0,
        'throttles': 0
    }
    
    log_summary = kestra_agent.summarize_cloudwatch_logs(healthy_logs)
    metrics_analysis = kestra_agent.analyze_lambda_metrics(healthy_metrics)
    kestra_decision = kestra_agent.make_deployment_decision(log_summary, metrics_analysis)
    rl_recommendation = rl_agent.optimize_deployment_strategy(healthy_metrics)
    
    print(f"Kestra Decision: {kestra_decision['action']} (confidence: {kestra_decision['confidence']:.2f})")
    print(f"RL Recommendation: {rl_recommendation['action']} (confidence: {rl_recommendation['confidence']:.2f})")
    print(f"Final Action: DEPLOY ✅")
    
    # Scenario 2: Critical errors
    print("\n\nScenario 2: Critical Errors Detected")
    print("-" * 40)
    
    critical_logs = [
        {'message': 'CRITICAL: Database connection lost'},
        {'message': 'ERROR: Failed to process request'},
        {'message': 'ERROR: Timeout exceeded'},
        {'message': 'FATAL: Service crashed'},
        {'message': 'ERROR: Memory exhausted'},
    ] * 4  # Multiply to exceed threshold
    
    critical_metrics = {
        'invocations': 1000,
        'errors': 150,
        'error_rate': 15.0,
        'duration': 8000,
        'cost': 200.0,
        'throttles': 20
    }
    
    log_summary = kestra_agent.summarize_cloudwatch_logs(critical_logs)
    metrics_analysis = kestra_agent.analyze_lambda_metrics(critical_metrics)
    kestra_decision = kestra_agent.make_deployment_decision(log_summary, metrics_analysis)
    
    print(f"Kestra Decision: {kestra_decision['action']} (confidence: {kestra_decision['confidence']:.2f})")
    print(f"Critical Issues: {len(log_summary.get('critical_errors_sample', []))}")
    print(f"Final Action: ROLLBACK 🔄")


def demo_workflow():
    """Demonstrate complete workflow."""
    print_section("Complete Pipeline Workflow Demo")
    
    print("Step 1: Collect metrics from AWS services")
    print("   └─ CloudWatch logs collected")
    print("   └─ Lambda metrics retrieved")
    
    print("\nStep 2: Kestra AI Agent analyzes data")
    print("   └─ Log patterns identified")
    print("   └─ Metrics evaluated")
    print("   └─ Decision recommended")
    
    print("\nStep 3: Oumi RL Agent provides optimization")
    print("   └─ Current state determined")
    print("   └─ Q-table consulted")
    print("   └─ Action recommended")
    
    print("\nStep 4: Orchestrator combines decisions")
    print("   └─ Priorities evaluated")
    print("   └─ Confidence calculated")
    print("   └─ Final action determined")
    
    print("\nStep 5: Execute action")
    print("   └─ Update DynamoDB state")
    print("   └─ Archive logs to S3")
    print("   └─ Trigger appropriate workflow")
    
    print("\nStep 6: Display results on dashboard")
    print("   └─ Real-time status updated")
    print("   └─ Metrics visualized")
    print("   └─ Decision reasoning shown")
    
    print("\n✅ Pipeline execution complete!")


def main():
    """Run all demos."""
    print("\n" + "🚀 AWS DevOps Pipeline Demo".center(60))
    print("Automated pipeline with Kestra AI Agent and Oumi RL".center(60))
    print("\n")
    
    try:
        # Run demonstrations
        demo_kestra_ai_agent()
        demo_rl_agent()
        demo_combined_decision()
        demo_workflow()
        
        print_section("Demo Complete")
        print("✨ This demo showed the key features of the AWS DevOps Pipeline:")
        print("   • Kestra AI Agent for intelligent log analysis")
        print("   • Oumi RL for deployment optimization")
        print("   • Combined decision-making process")
        print("   • Complete workflow orchestration")
        print("\n🎯 The system is ready for production deployment!")
        print("\nNext steps:")
        print("   1. Configure AWS credentials in .env")
        print("   2. Deploy backend API")
        print("   3. Deploy dashboard to Vercel")
        print("   4. Set up Kestra workflows")
        print("\n📚 See DEPLOYMENT.md for detailed instructions")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

"""
ARKHAM - CLI Entry Point
"""

import argparse
import sys

from .agent import CTFAgent


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="CTF Agent - AI-powered CTF assistant")
    parser.add_argument("--platform", choices=["htb", "thm", "pico", "custom"], 
                       default="custom", help="CTF platform")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Interactive mode")
    
    # Challenge commands
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("args", nargs="*", help="Arguments")
    
    args = parser.parse_args()
    
    agent = CTFAgent(platform=args.platform)
    
    if args.interactive:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║              🎯 ARKHAM v1.0 - Agent of Providence            ║
║                                                                  ║
║  «No puedo evitar sentir que hay algo más antiguo que los Dioses» ║
╚══════════════════════════════════════════════════════════════════╝

Commands:
    start <name> [options]  - Start new challenge
    run <command>           - Run shell command
    flag <flag>             - Submit found flag
    note <text>             - Add note
    suggest                 - Get next step suggestions
    report                  - Generate challenge report
    save                    - Save session
    load <session>          - Load previous session
    stats                   - Show statistics
    quit                    - Exit
        """)
        
        while True:
            try:
                user_input = input("arkham> ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split()
                cmd = parts[0].lower()
                
                if cmd in ("quit", "exit"):
                    break
                
                elif cmd == "start":
                    if len(parts) < 2:
                        print("Usage: start <name> [--category web] [--difficulty medium] [--ip x.x.x.x]")
                        continue
                    
                    name = parts[1]
                    category = "web" if "--web" in parts else "misc"
                    difficulty = "medium"
                    ip = None
                    
                    for i, p in enumerate(parts):
                        if p == "--category" and i+1 < len(parts):
                            category = parts[i+1]
                        if p == "--difficulty" and i+1 < len(parts):
                            difficulty = parts[i+1]
                        if p == "--ip" and i+1 < len(parts):
                            ip = parts[i+1]
                    
                    agent.start_challenge(name, category, difficulty, ip)
                    print(f"✅ Started: {name}")
                
                elif cmd == "run":
                    if len(parts) < 2:
                        print("Usage: run <command>")
                        continue
                    output = agent.run_command(" ".join(parts[1:]))
                    print(output[:500] if len(output) > 500 else output)
                
                elif cmd == "flag":
                    if len(parts) < 2:
                        print("Usage: flag <flag>")
                        continue
                    agent.add_flag(parts[1])
                    print("✅ Flag recorded!")
                
                elif cmd == "note":
                    if len(parts) < 2:
                        print("Usage: note <text>")
                        continue
                    agent.add_note(" ".join(parts[1:]))
                    print("✅ Note added!")
                
                elif cmd == "suggest":
                    suggestions = agent.suggest_next()
                    for s in suggestions:
                        print(f"  → {s}")
                
                elif cmd == "report":
                    print(agent.generate_report())
                
                elif cmd == "save":
                    result = agent.save_session()
                    if result:
                        print(f"✅ Session saved!")
                    else:
                        print("❌ Failed to save session")
                
                elif cmd == "load":
                    if len(parts) < 2:
                        print("Usage: load <session>")
                        continue
                    print(agent.load_session(parts[1]))
                
                elif cmd == "stats":
                    import json
                    stats = agent.get_stats()
                    print(f"""
📊 CTF Agent Statistics:
  🚩 Flags found: {stats['total_flags']}
  🎯 Challenges: {stats['total_challenges']}
  💾 Sessions: {stats['sessions_saved']}
  📁 Platform: {stats['platform']}
""")
                
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n👋 Bye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    else:
        # Single command mode
        if args.command == "stats":
            import json
            stats = agent.get_stats()
            print(json.dumps(stats, indent=2))
        else:
            print("Use --interactive for CLI mode")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

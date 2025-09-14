"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, Shield, Brain, Mic } from "lucide-react";

export function Hero() {
  return (
    <div className="flex flex-col lg:flex-row items-center justify-between gap-12 min-h-[80vh] py-20">
      {/* Left Content */}
      <div className="flex-1 space-y-8">
        <div className="space-y-4">
          <h1 className="text-4xl lg:text-6xl font-bold tracking-tight">
            Your AI{" "}
            <span className="text-personality">
              Voice Broker
            </span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Stop making stupid crypto trades. Let our AI voice agent research and invest for you like a seasoned Wall Street broker.
          </p>
        </div>

        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Shield className="h-4 w-4 text-personality" />
            <span>Research Before Trade</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Brain className="h-4 w-4 text-personality" />
            <span>AI-Powered Analysis</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Mic className="h-4 w-4 text-personality" />
            <span>Voice Commands</span>
          </div>
        </div>

        <div className="flex gap-4">
          <Button size="lg" className="bg-personality hover:bg-personality/90 text-black">
            Start Trading Smart
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
          <Button variant="outline" size="lg">
            Watch Demo
          </Button>
        </div>

        <p className="text-sm text-muted-foreground">
          "Like having Jordan Belfort in your pocket, but smarter and less likely to get you arrested."
        </p>
      </div>

      {/* Right Phone Preview */}
      <div className="flex-1 flex justify-center">
        <div className="relative">
          {/* Phone Frame */}
          <div className="w-64 h-[500px] bg-gray-900 rounded-[2.5rem] p-2 shadow-2xl">
            <div className="w-full h-full bg-black rounded-[2rem] overflow-hidden relative">
              {/* Screen Content */}
              <div className="absolute inset-0 bg-personality/10">
                <div className="p-6 h-full flex flex-col justify-between">
                  {/* Header */}
                  <div className="text-center">
                    <div className="w-12 h-12 bg-personality rounded-full mx-auto mb-3 flex items-center justify-center">
                      <Mic className="h-6 w-6 text-black" />
                    </div>
                    <h3 className="text-white font-semibold text-lg">PocketBroker</h3>
                    <p className="text-gray-400 text-sm">AI Voice Agent</p>
                  </div>

                  {/* Middle Content */}
                  <div className="space-y-4">
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                      <p className="text-white text-sm">
                        "Hey PocketBroker, should I buy Bitcoin?"
                      </p>
                    </div>
                    <div className="bg-personality/20 backdrop-blur-sm rounded-lg p-4">
                      <p className="text-white text-sm">
                        "Based on market analysis, Bitcoin shows strong support at $42K. Consider a small position..."
                      </p>
                    </div>
                  </div>

                  {/* Bottom */}
                  <div className="text-center">
                    <div className="w-8 h-8 bg-personality rounded-full mx-auto"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Floating Elements */}
          <div className="absolute -top-4 -right-4 w-8 h-8 bg-personality rounded-full animate-pulse"></div>
          <div className="absolute -bottom-4 -left-4 w-6 h-6 bg-personality rounded-full animate-pulse delay-1000"></div>
        </div>
      </div>
    </div>
  );
}
